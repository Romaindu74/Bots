from ..GetLang          import Code, Get_User_Lang
from ..Logger           import Logger
from ..Utils            import send
from ..type.Bot         import Bot

_log = Logger(__name__)

try:
    import discord
    from discord.ext    import commands
except ImportError:
    _log.Critical(Code('0.0.0.0.0').format(Module = 'discord'), Exit = True)
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

class DiscordError(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.client = Bot.Client

    @commands.Cog.listener(
        name = "on_command_error"
    )
    async def _on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if not ctx.author.bot:
            if isinstance(error, commands.CommandNotFound): 
                await send(ctx, embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get('0.0.0.0.2'), description = Get_User_Lang(ctx.author.id).get('0.0.0.0.3'), color = ctx.author.color), reference=False)
                return

            if isinstance(error, discord.Forbidden):
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.0.4'), reference=False)
                return

            _log.Warn(Get_User_Lang(ctx.author.id).get('0.0.0.0.5').format(command = ctx.message.content, error = error))
            await send(ctx, embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get('0.0.0.0.6'), description = Get_User_Lang(ctx.author.id).get('0.0.0.0.7').format(error = error)), reference=False)

async def setup(Bot: Bot) -> bool:
    _cog = DiscordError(Bot)
    try:
        _log.Info(Code('0.0.0.0.8').format(cog = _cog.__class__.__name__))
        await Bot.Client.add_cog(_cog)
    except Exception:
        _log.Warn(Code('0.0.0.0.9').format(cog = _cog.__class__.__name__))
        return False
    else:
        _log.Info(Code('0.0.0.1.0').format(cog = _cog.__class__.__name__))
        return True