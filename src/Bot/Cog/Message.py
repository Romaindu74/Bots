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
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.8.8'))

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
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.8.9'), reference=False)
                return

            await ctx.message.delete()
            await send(ctx, message = message, reference=False)
            return True

        if await self._check(ctx, message):
            if not message:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.8.9'), reference=False)
                return

            await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.9.0').format(Mention = ctx.author.mention, Message = message), reference=False)

async def setup(Bot: Bot) -> bool:
    try:
        await Bot.Client.add_cog(Message(Bot))
    except Exception:
        return False
    else:
        return True

