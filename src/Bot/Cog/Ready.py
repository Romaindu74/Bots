from ..GetLang          import Code
from ..Logger           import Logger
from ..Utils            import Save
from ..type.Bot         import Bot

_log = Logger(__name__)

import os
import asyncio

try:
    from discord.ext    import commands
except ImportError:
    _log.Critical(Code('0.0.0.0.0').format(Module = 'discord'), Exit = True)
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

class Ready(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.Bot       = Bot
        self.client    = self.Bot.Client
        self.Interface = self.Bot.Interface
        self.options   = self.Bot.Options

        self.ping      = False

    async def _ping(self) -> None:
        while True:
            try:
                self.Bot.Status.UpDate_Ping((self.client.latency * 1000))
            except:
                pass

            await asyncio.sleep(1)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        _log.Info(Code('0.0.0.3.2'))
        os.makedirs(self.options.Path+'/User/Bots/Images/', exist_ok = True)
        avatar = self.client.user.avatar
        if avatar is not None:
            await avatar.save(self.options.Path+'/User/Bots/Images/{0}.png'.format(str(self.client.user.id)))

        self.Bot.Info['Id'] = str(self.client.user.id)
        self.Bot.Info['Name'] = str(self.client.user.name)

        Save('{0}/User/Bots/{1}/Main.json'.format(self.options.Path, self.Bot.Id), self.Bot.Info)

        if not self.ping:
            self.ping = True
            self.client.loop.create_task(self._ping())

        self.Bot.Status_ = '0.0.0.3.2'
        self.Interface.UpDate_Bot(str(self.client.user.id))


    @commands.Cog.listener()
    async def on_disconnect(self) -> None:
        _log.Info(Code('0.0.0.3.3'))
        self.Bot.Status_ = '0.0.0.3.3'
        self.Interface.UpDate_Bot(str(self.client.user.id))

    @commands.Cog.listener()
    async def on_connect(self) -> None:
        _log.Info(Code('0.0.0.3.4'))
        self.Bot.Status_ = '0.0.0.3.4'
        self.Interface.UpDate_Bot(str(self.client.user.id))

    @commands.Cog.listener()
    async def on_resumed(self) -> None:
        _log.Info(Code('0.0.0.3.5'))
        self.Bot.Status_ = '0.0.0.3.5'
        self.Interface.UpDate_Bot(str(self.client.user.id))

async def setup(Bot: Bot) -> bool:
    _cog = Ready(Bot)
    try:
        _log.Info(Code('0.0.0.0.8').format(cog = _cog.__class__.__name__))
        await Bot.Client.add_cog(_cog)
    except Exception:
        _log.Warn(Code('0.0.0.0.9').format(cog = _cog.__class__.__name__))
        return False
    else:
        _log.Info(Code('0.0.0.1.0').format(cog = _cog.__class__.__name__))
        return True