from .Logger         import Logger
from .AddCog         import AddCog
from .GetLang        import Code

from .type.Interface import Interface as _Interface
from .type.Options   import Options   as _Options
from .Status         import Status    as _Status
from .Loop           import Loop      as _Loop

from .Utils          import Open, MISSING

from time            import sleep

import os, asyncio
import threading

_log = Logger(__name__)

try:
    import discord
    from discord.ext import commands
except ImportError:
    _log.Critical(Code('0.0.0.0.0').format(Module = 'discord'), Exit = True)
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

class Bot(threading.Thread):
    _initialized: bool = False
    _error      : bool = False

    def __init__(self, Id: str = MISSING, Options: _Options = MISSING) -> None:
        super(Bot, self).__init__()
        if Id == MISSING:
            _log.Critical(Code('0.0.0.9.9').format(bot = Id, error = Code('0.0.1.0.0')))
            self._error = True
            return

        elif Options == MISSING:
            _log.Critical(Code('0.0.0.9.9').format(bot = Id, error = Code('0.0.1.0.1')))
            self._error = True
            return

        _log.Info(Code('0.0.1.0.4').format(bot = Id))

        self._event: int            = 0
        self._interface: _Interface = None

        self._id: str               = Id
        self._options: _Options     = Options

        self._status: _Status       = _Status(self, self._options)
        self._loop: _Loop           = _Loop(self)

        _log.Info(Code('0.0.1.0.2'))
        if not os.path.exists('{0}/User/Bots/{1}/'.format(self._options.Path, self._id)):
            os.makedirs('{0}/User/Bots/{1}/'.format(self._options.Path, self._id), exist_ok = True)

        self._prefix: dict          = Open('{0}/User/Bots/{1}/Prefix.json'.format(self._options.Path, self._id), {'Prefix': ["!"]})
        self._info: dict            = Open('{0}/User/Bots/{1}/Main.json'.format(self._options.Path, self._id))
        _log.Info(Code('0.0.1.0.3'))

        self._status_: str          = '0.0.0.3.3'
        self._client: commands.Bot  = None
        self._ping: float           = 0.0

        self._initialized: bool     = True
        _log.Info(Code('0.0.1.0.5'))

    def run(self) -> None:
        while True:
            if self._event == 0:
                sleep(0.5)
            elif self._event == 1:
                self._event = 0
                asyncio.run(self._Start())

    async def _Start(self) -> None:
        if not self._initialized:
            _log.Warn(Code('0.0.1.0.6'))
            return

        if not self.Info.get('Token', False):
            _log.Warn(Code('0.0.1.0.7'))
            return

        try:
            _log.Info(Code('0.0.1.0.8'))
            self.Client = commands.Bot((self._prefix_), intents = discord.Intents.all())
        except discord.errors.PrivilegedIntentsRequired:
            _log.Info(Code('0.0.1.0.9'))
            self.Client = commands.Bot((self._prefix_))

        if not await AddCog(self):
            _log.Warn(Code('0.0.1.1.0'))

        try:
            _log.Info(Code('0.0.1.1.1'))
            self.Status.Start()
        except Exception:
            _log.Error(Code('0.0.1.1.2'))
        else:
            _log.Info(Code('0.0.1.1.3'))
    
        try:
            _log.Info(Code('0.0.1.1.4'))
            self._loop.start()
        except Exception:
            _log.Error(Code('0.0.1.1.5'))
        else:
            _log.Info(Code('0.0.1.1.6'))

        try:
            _log.Info(Code('0.0.1.1.7'))
            await self.Client.start(self.Info.get('Token'))
        except KeyboardInterrupt:
            _log.Critical(Code('0.0.1.1.8'))
            self.Client.loop.create_task(self.Client.close())
        except Exception as e:
            _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)))

    def _prefix_(self, client: commands.Bot, message: discord.Message) -> list:
        _prefix: list = []

        for prefix in self.Prefix.get('Prefix', []):
            _prefix.append(prefix)

        if message.guild:
            if not os.path.exists('{0}/User/{1}/__Guilds__/{2}/'.format(self._options.Path, client.user.id, message.guild.id)):
                os.makedirs('{0}/User/{1}/__Guilds__/{2}/'.format(self._options.Path, client.user.id, message.guild.id), exist_ok = True)

            guild_prefix: dict = Open('{0}/User/{1}/__Guilds__/{2}/Main.json'.format(self._options.Path, client.user.id, message.guild.id), {'Prefix': []})
            for prefix in guild_prefix:
                _prefix.append(prefix)

        return _prefix

    def Stop(self) -> bool:
        if self.Status == '0.0.0.3.3':
            _log.Warn(Code('0.0.1.1.9'))
            return False

        if self.Client == None:
            _log.Error(Code('0.0.1.2.0'))
            return False

        try:
            _log.Info(Code('0.0.1.2.1'))
            self.Status.Stop()
        except Exception:
            _log.Error(Code('0.0.1.2.2'))
        else:
            _log.Info(Code('0.0.1.2.3'))
    
        try:
            _log.Info(Code('0.0.1.2.4'))
            self._loop.stop()
        except Exception:
            _log.Error(Code('0.0.1.2.5'))
        else:
            _log.Info(Code('0.0.1.2.6'))

        try:
            _log.Info(Code('0.0.1.2.7'))
            self.Client.loop.create_task(self.Client.close())
        except Exception:
            _log.Info(Code('0.0.1.2.8'))
            return False
        
        else:
            _log.Info(Code('0.0.1.2.9'))
            self.Status_ = '0.0.0.3.3'
            self.Interface.UpDate_Bot(self.Id)
            self.Client = None

            return True

    def Start(self) -> bool:
        try:
            self._event = 1
        except Exception:
            return False
        else:
            return True

    @property
    def Initialized(self) -> bool:
        return self._initialized

    @property
    def Error(self) -> bool:
        return self._error

    @property
    def Interface(self) -> _Interface:
        return self._interface

    @Interface.setter
    def Interface(self, value: _Interface = MISSING) -> _Interface:
        if value:
            self._interface = value

        return self._interface

    @property
    def Id(self) -> str:
        return self._id

    @Id.setter
    def Id(self, value: str = MISSING) -> str:
        if value:
            self._id = value

        return self._id

    @property
    def Options(self) -> _Options:
        return self._options

    @Options.setter
    def Options(self, value: _Options = MISSING) -> _Options:
        if value:
            self._options = value

        return self._options

    @property
    def Status(self) -> _Status:
        return self._status

    @Status.setter
    def Status(self, value: _Status = MISSING) -> _Status:
        if value:
            self._status = value

        return self._status

    @property
    def Prefix(self) -> dict:
        return self._prefix

    @Prefix.setter
    def Prefix(self, value: dict = MISSING) -> dict:
        if value:
            self._prefix = value

        return self._prefix

    @property
    def Info(self) -> dict:
        return self._info

    @Info.setter
    def Info(self, value: dict = MISSING) -> dict:
        if value:
            self._info = value

        return self._info

    @property
    def Status_(self) -> str:
        return self._status_

    @Status_.setter
    def Status_(self, value: str = MISSING) -> str:
        if value:
            self._status_ = value

        return self._status_

    @property
    def Client(self) -> commands.Bot:
        return self._client

    @Client.setter
    def Client(self, value: commands.Bot = MISSING) -> commands.Bot:
        if value:
            self._client = value

        return self._client

    @property
    def Ping(self) -> float:
        return self._ping

    @Ping.setter
    def Ping(self, value: float = MISSING) -> float:
        if value:
            self._ping = value

        return self._ping