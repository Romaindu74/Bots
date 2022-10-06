from ..GetLang import Get_Lang
from ..type.Bot import Bot
from ..Logger  import Log
from ..Utils   import Open

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
    try:
        await Bot.Client.add_cog(Member_Join(Bot))
    except Exception:
        return False
    else:
        return True