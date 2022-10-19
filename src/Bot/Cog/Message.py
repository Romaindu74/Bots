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

class Message(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
            self.Bot     = Bot

            self.client  = self.Bot.Client

    async def _check(self, ctx: commands.Context, message: str) -> bool:
        if not ctx.author.bot:
            if not '@' in message:
                await ctx.message.delete()
                return True
            else:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.5.6'))

    @commands.command(
        name = "message",
        aliases = [
            "Message", "mEssage", "meSsage", "mesSage", "messAge", "messaGe", "messagE", "MESSAGE"
            "Msg", "mSg", "msG",
            "MSg", "mSG", "MsG",
            "msg", "MSG"
            ]
        )
    async def _message(self, ctx: commands.Context, *, message: str = False) -> None:
        if str(ctx.author.id) in self.Bot.Info.get('Owner', []):
            if not message:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.5.7'), reference=False)
                return

            await ctx.message.delete()
            await send(ctx, message = message, reference=False)
            return True

        if await self._check(ctx, message):
            if not message:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.5.7'), reference=False)
                return

            await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.9.0').format(mention = ctx.author.mention, message = message), reference=False)

async def setup(Bot: Bot) -> bool:
    _cog = Message(Bot)
    try:
        _log.Info(Code('0.0.0.0.8').format(cog = _cog.__class__.__name__))
        await Bot.Client.add_cog(_cog)
    except Exception:
        _log.Warn(Code('0.0.0.0.9').format(cog = _cog.__class__.__name__))
        return False
    else:
        _log.Info(Code('0.0.0.1.0').format(cog = _cog.__class__.__name__))
        return True