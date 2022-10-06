from ..GetLang import Get_Lang, Get_User_Lang
from ..type.Bot import Bot
from ..Logger  import Log
from ..Utils   import send, purge

try:
    import discord
    from discord.ext import commands
except ImportError:
    Log(50, Get_Lang.get('0.0.0.0.0').format(Name = 'discord'), True)
except Exception as e:
    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)

__all__ = (
    'setup'
)

class Purge(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.Bot    = Bot
        self.client = self.Bot.Client

    async def _check(self, ctx: commands.Context) -> bool:
        if ctx.author.bot == False:
            if not (ctx.guild):
                await send(ctx, message =  Get_User_Lang(ctx.author.id).get("0.0.0.9.3"))
                return False
            else:
                if ctx.author.guild_permissions.manage_messages:
                    return True
                else:
                    await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.8.0"))
                    return False

    @commands.command(name = "Purge", aliases = ["purge"])
    async def _purge(self, ctx: commands.Context, nombre: int = False) -> None:
        if await self._check(ctx):
            if (not nombre) or  not (0 < nombre < 1000):
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.1.0.5"))
            else:
                await purge(ctx, nombre)
                message = await send(ctx, embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.1.0.6").format(N = nombre, Name = ctx.author.name), color = ctx.author.color), reference = False)
                await message.delete(delay=5)

async def setup(Bot: Bot) -> bool:
    try:
        await Bot.Client.add_cog(Purge(Bot))
    except Exception:
        return False
    else:
        return True