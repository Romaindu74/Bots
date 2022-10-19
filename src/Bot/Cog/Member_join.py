from ..GetLang          import Code
from ..Logger           import Logger
from ..Utils            import Open
from ..type.Bot         import Bot

_log = Logger(__name__)

try:
    import discord
    from discord.ext    import commands
except ImportError:
    _log.Critical(Code('0.0.0.0.0').format(Module = 'discord'), Exit = True)
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

class Member_Join(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.Bot     = Bot
        self.client  = self.Bot.Client
        self.options = self.Bot.Options

        self.path = '{0}/User/{1}/__Guilds__/'.format(self.options.Path, self.Bot.Id)

    @commands.Cog.listener(
        name = "on_member_join"
    )
    async def _member_add(self, member: discord.Member) -> None:
        Guild = Open('{0}{1}/Main.json'.format(self.path, member.guild.id))

        if Guild.get('Member-Join', False):
            for info in Guild['Member-Join']:
                channel = self.client.get_channel(int(info['Channel']))
                message = info['Message'].format(name = member.name, mention = member.mention, id = member.id)
                await channel.send(message)

    @commands.Cog.listener(
        name = "on_member_leave"
    )
    async def _member_leave(self, member: discord.Member) -> None:
        Guild = Open('{0}{1}/Main.json'.format(self.path, member.guild.id))

        if Guild.get('Member-Leave', False):
            for info in Guild['Member-Leave']:
                channel = self.client.get_channel(int(info['Channel']))
                message = info['Message'].format(name = member.name, mention = member.mention, id = member.id)
                await channel.send(message)

async def setup(Bot: Bot) -> bool:
    _cog = Member_Join(Bot)
    try:
        _log.Info(Code('0.0.0.0.8').format(cog = _cog.__class__.__name__))
        await Bot.Client.add_cog(_cog)
    except Exception:
        _log.Warn(Code('0.0.0.0.9').format(cog = _cog.__class__.__name__))
        return False
    else:
        _log.Info(Code('0.0.0.1.0').format(cog = _cog.__class__.__name__))
        return True