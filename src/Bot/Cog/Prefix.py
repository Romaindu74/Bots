from ..GetLang import Get_Lang, Get_User_Lang
from ..type.Bot import Bot
from ..Logger  import Log
from ..Utils   import send, Open, Save

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

class Prefix(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.Bot    = Bot
        self.path   = '{0}/User/{1}/__Guilds__/'.format(self.Bot.Options.Path, self.Bot.Id)

    async def _check(slef, ctx: commands.Context) -> bool:
        if not ctx.author.bot:
            if not (ctx.guild):
                await send(ctx, message =  Get_User_Lang(ctx.author.id).get("0.0.0.9.3"))
                return False
            return True
        else:
            return False


    @commands.command(
        name = "new-prefix",
        aliases = [
            "New-Prefix","new-Prefix","New-prefix"
        ]
    )
    async def _new_prefix(self, ctx: commands.Context, *, prefix: str = False) -> None:
        if await self._check(ctx):
            if not prefix:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.9.9"))
                return False

            Guild = Open('{0}/{1}/Main.json'.format(self.path, ctx.guild.id))

            if not 'Prefix' in Guild:
                Guild['Prefix'] = []

            if not prefix in Guild.get('Prefix'):
                Guild['Prefix'].append(prefix)

            Save('{0}/{1}/Main.json'.format(self.path, ctx.guild.id), Guild)
            await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.1.0.0").format(Prefix = prefix))

    @commands.command(
        name = "remove-prefix",
        aliases = [
            "Remove-Prefix",
            "remove-Prefix",
            "Remove-prefix"
        ]
    )
    async def _remove_prefix(self, ctx: commands.Context, *, prefix: str = False) -> None:
        if await self._check(ctx):
            if not prefix:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.9.9"))
                return False

            Guild = Open('{0}/{1}/Main.json'.format(self.path, ctx.guild.id))

            if not 'Prefix' in Guild:
                Guild['Prefix'] = []

            if not prefix in Guild.get('Prefix'):
                Guild['Prefix'].remove(prefix)

            Save('{0}/{1}/Main.json'.format(self.path, ctx.guild.id), Guild)
            await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.1.0.1").format(Prefix = prefix))

    @commands.command(
        name = "view-prefix",
        aliases = [
            "View-Prefix",
            "view-Prefix",
            "View-prefix"
        ]
    )
    async def _all_prefix(self, ctx: commands.Context, *, page: int = 1) -> None:
        if await self._check(ctx):
            Guild = Open('{0}/{1}/Main.json'.format(self.path, ctx.guild.id))

            if not 'Prefix' in Guild:
                Guild['Prefix'] = []

            index = 0
            embed = discord.Embed()
            value = ''

            for prefix in Guild.get('Prefix'):
                index += 1
                if ((page - 1)*20) < index < ((page*20)):
                    value += '({0})-{1}: `{2}`\n'.format(index, Get_User_Lang(ctx.author.id).get("0.0.1.0.2"), prefix)

            if value == '':
                value = Get_User_Lang(ctx.author.id).get("0.0.1.0.3")

            embed.add_field(name = Get_User_Lang(ctx.author.id).get("0.0.1.0.4"), value = value, inline = False)

            pages = int(len(Guild.get('Prefix'))/20)
            if (len(Guild.get('Prefix'))/20) >= 0.1:
                pages += 1
            
            embed.set_footer(text = Get_User_Lang(ctx.author.id).get("0.0.0.4.5").format(Page = page, Pages = pages))
            await send(ctx, embed = embed)

async def setup(Bot: Bot) -> bool:
    try:
        await Bot.Client.add_cog(Prefix(Bot))
    except Exception:
        return False
    else:
        return True