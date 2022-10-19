from ..GetLang          import Code, Get_User_Lang
from ..Logger           import Logger
from ..Utils            import send
from ..type.Bot         import Bot

_log = Logger(__name__)

try:
    from discord.ext    import commands
except ImportError:
    _log.Critical(Code('0.0.0.0.0').format(Module = 'discord'), Exit = True)
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

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
            msg = await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.2.1").format(ping = round(self.Bot.Client.latency * 1000)))
            await msg.add_reaction("🏓")

async def setup(Bot: Bot) -> bool:
    _cog = Ping(Bot)
    try:
        _log.Info(Code('0.0.0.0.8').format(cog = _cog.__class__.__name__))
        await Bot.Client.add_cog(_cog)
    except Exception:
        _log.Warn(Code('0.0.0.0.9').format(cog = _cog.__class__.__name__))
        return False
    else:
        _log.Info(Code('0.0.0.1.0').format(cog = _cog.__class__.__name__))
        return True