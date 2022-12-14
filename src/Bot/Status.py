from .Utils        import MISSING, Open, Save
from .type.Bot     import Bot
from .type.Options import Options
from .Logger       import Logger
from .GetLang      import Code

_log = Logger(__name__)

import asyncio
import threading
import tkinter as tk

try:
    import discord
except ImportError:
    _log.Error(Code('0.0.0.0.0').format(Module = 'discord'))
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

Types = [
    'Joue à',
    'En direct sur Twith',
    'Ecoute',
    'Regarde',
    '?????',
    'Participant à'
]

Status_ = {
    'online'    : 'En ligne',
    'offline'   : 'Hors ligne',
    'idle'      : 'Inactif',
    'dnd'       : 'Ne pas déranger',
    'dnd'       : 'Ne pas déranger',
    'invisible' : 'Invisible'
}

class Status:
    def __init__(self, Bot: Bot, Options: Options) -> None:
        self.proccess = None
        self.Bot     = Bot
        self.Options = Options

        self.activite_ = None
        self.statu_    = None
        self.time_     = None
        self.ping_     = None

    def Interface(self, Activite: tk.Label, Statu: tk.Label, Time: tk.Label, Ping: tk.Label) -> None:
        _log.Info(Code('0.0.2.4.5'))
        self.activite_ = Activite
        self.statu_    = Statu
        self.time_     = Time
        self.ping_     = Ping
        _log.Info(Code('0.0.2.4.6'))

    def Start(self) -> None:
        _log.Info(Code('0.0.2.4.7'))
        process = Start(self.Bot, self.Options, self)

        process.start()
        self.proccess = process
        _log.Info(Code('0.0.2.4.8'))

    def Stop(self) -> None:
        _log.Info(Code('0.0.2.4.9'))
        if self.proccess:
            self.proccess.stop()
        
        self.proccess = None
        _log.Info(Code('0.0.2.5.0'))

    def UpDate_Ping(self, ms: float = MISSING) -> None:
        ms = round(ms, 2)
        self.Bot.Ping = ms
        if self.proccess:
            if self.proccess.is_config and self.ping_:
                self.ping_.config(text = Code('0.0.1.8.0').format(ping = ms))

    @property
    def Activity(self) -> str:
        if self.proccess:
            return Types[self.proccess.current.get("Type", 0)]
        return ''

    @property
    def Text(self) -> str:
        if self.proccess:
            return self.proccess.current.get("Text", '')
        return ''

    @property
    def Statu(self) -> str:
        if self.proccess:
            return Status_[self.proccess.current.get("Status", 'online')]
        return ''

    @property
    def Time(self) -> int:
        return 0

    @property
    def Is_Config(self) -> bool:
        if self.proccess == None:
            return False
        return self.proccess.is_config

    @Is_Config.setter
    def Is_Config(self, value: bool) -> bool:
        if self.proccess == None:
            return False
        self.proccess.is_config = value
        return self.proccess.is_config

class Start(threading.Thread):
    def __init__(self, Bot: Bot, Options: Options, main: Status) -> None:
        super(Start, self).__init__()
        self.Bot     = Bot
        self.Options = Options

        self.current   = {}

        self.stop_     = False

        self.is_config = False

        self.main: Status = main

    def run(self):
        """
            TYPE
            ----------------------------------------------------------------
                playing            = 0 =             Joue à
                streaming          = 1 =             En direct sur Twith
                listening          = 2 =             Ecoute
                watching           = 3 =             Regarde
                custom             = 4 =             ?????
                competing          = 5 =             Participant à
            ----------------------------------------------------------------
            STATU
            ----------------------------------------------------------------
                online            = 'online'    =     En ligne
                offline           = 'offline'   =     Hors ligne
                idle              = 'idle'      =     Inactif
                dnd               = 'dnd'       =     Ne pas déranger
                do_not_disturb    = 'dnd'       =     Ne pas déranger
                invisible         = 'invisible' =     Invisible
            ----------------------------------------------------------------
        """
        asyncio.run(self.run_())

    async def run_(self):
        while True:
            if self.stop_:
                break

            Statu = Open('{0}/User/Bots/{1}/Status.json'.format(self.Options.Path, self.Bot.Id), {'Status': []})
            if not 'Status' in Statu:
                Statu['Status'] = []
                Save('{0}/User/Bots/{1}/Status.json'.format(self.Options.Path, self.Bot.Id), Statu)

            if Statu.get('Status', []) != []:
                for i in Statu.get('Status', []):
                    self.current = i

                    try:
                        await self.Bot.Client.change_presence(
                            activity = discord.Activity(
                                type = i.get("Type", 0),
                                name = i.get("Text", "")
                            ),
                            status = i.get("Status", "online")
                        )

                    except AttributeError:
                        pass

                    except Exception as e:
                        if not self.stop_:
                            _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)))

                    else:
                        if self.main.activite_ and self.main.statu_ and self.is_config:
                            try:
                                self.main.activite_.config(text = Code('0.0.1.8.2').format(activity = Types[i.get("Type", 0)], text = i.get("Text", "")))
                                self.main.statu_.config(text    = Code('0.0.1.8.3').format(display  = Status_[i.get("Status", "online")]))
                            except:
                                self.is_config = False

                        for time in range(i.get('Sleep', 0)):
                            if self.stop_:
                                break

                            if self.main.time_ and self.is_config:
                                try:
                                    self.main.time_.config(text = Code('0.0.1.8.4').format(time = (i.get('Sleep', 0)-1)-time))
                                except:
                                    self.is_config = False
                            await asyncio.sleep(1)

            else:
                await asyncio.sleep(5)

    def stop(self) -> None:
        self.stop_ = True