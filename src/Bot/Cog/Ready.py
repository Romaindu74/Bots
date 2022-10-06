from ..Utils    import Save
from ..GetLang  import Get_Lang
from ..type.Bot import Bot
from ..Logger   import Log
import os

try:
    from discord.ext import commands
except ImportError:
    Log(50, Get_Lang.get('0.0.0.0.0').format(Name = 'discord'), True)
except Exception as e:
    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)

try:
    import asyncio
except ImportError:
    Log(50, Get_Lang.get('0.0.0.0.0').format(Name = 'asyncio'), True)
except Exception as e:
    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)

__all__ = (
    'setup'
)

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
        try:
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

            self.Bot.Status_ = '0.0.0.6.1'
            self.Interface.UpDate_Bot(str(self.client.user.id))
        except Exception as e:
            Log(50, str(e))


    @commands.Cog.listener()
    async def on_disconnect(self) -> None:
        self.Bot.Status_ = '0.0.0.6.2'
        self.Interface.UpDate_Bot(str(self.client.user.id))

    @commands.Cog.listener()
    async def on_connect(self) -> None:
        self.Bot.Status_ = '0.0.0.6.3'
        self.Interface.UpDate_Bot(str(self.client.user.id))

    @commands.Cog.listener()
    async def on_resumed(self) -> None:
        self.Bot.Status_ = '0.0.0.6.4'
        self.Interface.UpDate_Bot(str(self.client.user.id))

async def setup(Bot: Bot) -> bool:
    try:
        await Bot.Client.add_cog(Ready(Bot))
    except Exception:
        return False
    else:
        return True
