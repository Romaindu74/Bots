from ..GetLang          import Code, Get_User_Lang
from ..Utils            import send, Open, Save
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

class Prefix(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.Bot    = Bot
        self.path   = '{0}/User/{1}/__Guilds__/'.format(self.Bot.Options.Path, self.Bot.Id)

    async def _check(slef, ctx: commands.Context) -> bool:
        if not ctx.author.bot:
            if not (ctx.guild):
                await send(ctx, message =  Get_User_Lang(ctx.author.id).get("0.0.0.2.2"))
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
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.2.3"))
                return False

            Guild = Open('{0}/{1}/Main.json'.format(self.path, ctx.guild.id))

            if not 'Prefix' in Guild:
                Guild['Prefix'] = []

            if not prefix in Guild.get('Prefix'):
                Guild['Prefix'].append(prefix)

            Save('{0}/{1}/Main.json'.format(self.path, ctx.guild.id), Guild)
            await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.2.4").format(prefix = prefix))

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
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.2.3"))
                return False

            Guild = Open('{0}/{1}/Main.json'.format(self.path, ctx.guild.id))

            if not 'Prefix' in Guild:
                Guild['Prefix'] = []

            if not prefix in Guild.get('Prefix'):
                Guild['Prefix'].remove(prefix)

            Save('{0}/{1}/Main.json'.format(self.path, ctx.guild.id), Guild)
            await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.2.5").format(prefix = prefix))

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
                    value += '({0})-{1}: `{2}`\n'.format(index, Get_User_Lang(ctx.author.id).get("0.0.0.2.6"), prefix)

            if value == '':
                value = Get_User_Lang(ctx.author.id).get("0.0.0.2.7")

            embed.add_field(name = Get_User_Lang(ctx.author.id).get("0.0.0.2.8"), value = value, inline = False)

            pages = int(len(Guild.get('Prefix'))/20)
            if (len(Guild.get('Prefix'))/20) >= 0.1:
                pages += 1
            
            embed.set_footer(text = Get_User_Lang(ctx.author.id).get("0.0.0.2.9").format(page = page, pages = pages))
            await send(ctx, embed = embed)

async def setup(Bot: Bot) -> bool:
    _cog = Prefix(Bot)
    try:
        _log.Info(Code('0.0.0.0.8').format(cog = _cog.__class__.__name__))
        await Bot.Client.add_cog(_cog)
    except Exception:
        _log.Warn(Code('0.0.0.0.9').format(cog = _cog.__class__.__name__))
        return False
    else:
        _log.Info(Code('0.0.0.1.0').format(cog = _cog.__class__.__name__))
        return True