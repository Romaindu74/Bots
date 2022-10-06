from ..GetLang import Get_Lang, Get_User_Lang
from ..type.Bot import Bot
from ..Logger  import Log
from ..Utils   import send

try:
    from discord.ext import commands
except ImportError:
    Log(50, Get_Lang.get('0.0.0.0.0').format(Name = 'discord'), True)
except Exception as e:
    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)

__all__ = (
    'setup'
)


class Ping(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
            self.Bot = Bot

    async def _check(self, ctx: commands.Context) -> bool:
        if not ctx.author.bot:
            return True

    @commands.command(
        name = "ping",
        aliases = [
            "Ping", "pIng", "piNg", "pinG",
            "PIng", "pINg", "piNG", "PinG",
            "PINg", "pING", "PiNG", "PInG",
            "PING"
            ]
        )
    async def _ping(self, ctx: commands.Context) -> None:
        if await self._check(ctx):
            msg = await send(ctx, message = "{0} **{1} ms**".format(Get_User_Lang(ctx.author.id).get("0.0.0.9.8"), round(self.Bot.Client.latency * 1000)))
            await msg.add_reaction("🏓")

async def setup(Bot: Bot) -> bool:
    try:
        await Bot.Client.add_cog(Ping(Bot))
    except Exception:
        return False
    else:
        return True