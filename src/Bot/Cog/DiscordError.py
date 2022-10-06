from ..GetLang  import Get_Lang, Get_User_Lang
from ..type.Bot import Bot
from ..Logger   import Log
from ..Utils    import send

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

class DiscordError(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.client = Bot.Client

    @commands.Cog.listener(
        name = "on_command_error"
    )
    async def _on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if not ctx.author.bot:
            if isinstance(error, commands.CommandNotFound): 
                await send(ctx, embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get('0.0.0.7.5'), description = Get_User_Lang(ctx.author.id).get('0.0.0.7.6'), color = ctx.author.color), reference=False)
                return
            Log(30, Get_User_Lang(ctx.author.id).get('0.0.0.7.7').format(Error = error))
            await send(ctx, embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get('0.0.0.7.8'), description = Get_User_Lang(ctx.author.id).get('0.0.0.7.9').format(Error = error)), reference=False)

async def setup(Bot: Bot) -> bool:
    try:
        await Bot.Client.add_cog(DiscordError(Bot))
    except Exception:
        return False
    else:
        return True