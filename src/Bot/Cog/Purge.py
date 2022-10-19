from ..GetLang          import Code, Get_User_Lang
from ..Utils            import send, purge
from ..Logger           import Logger
from ..type.Bot         import Bot

_log = Logger(__name__)

try:
    import discord
    from discord.ext    import commands
except ImportError:
    _log.Critical(Code('0.0.0.0.0').format(Module = 'discord'), Exit = True)
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

class Purge(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.Bot    = Bot
        self.client = self.Bot.Client

    async def _check(self, ctx: commands.Context) -> bool:
        if ctx.author.bot == False:
            if not (ctx.guild):
                await send(ctx, message =  Get_User_Lang(ctx.author.id).get("0.0.0.2.2"))
                return False
            else:
                if ctx.author.guild_permissions.manage_messages:
                    return True
                else:
                    await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.1.1"))
                    return False

    @commands.command(name = "Purge", aliases = ["purge"])
    async def _purge(self, ctx: commands.Context, nombre: int = False) -> None:
        if await self._check(ctx):
            if (not nombre) or  not (0 < nombre < 1000):
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.3.0"))
            else:
                await purge(ctx, nombre)
                message = await send(ctx, embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.0.3.1").format(number = nombre, member = ctx.author.name), color = ctx.author.color), reference = False)
                await message.delete(delay=5)

async def setup(Bot: Bot) -> bool:
    _cog = Purge(Bot)
    try:
        _log.Info(Code('0.0.0.0.8').format(cog = _cog.__class__.__name__))
        await Bot.Client.add_cog(_cog)
    except Exception:
        _log.Warn(Code('0.0.0.0.9').format(cog = _cog.__class__.__name__))
        return False
    else:
        _log.Info(Code('0.0.0.1.0').format(cog = _cog.__class__.__name__))
        return True