from ..Utils   import Open, Save
from ..GetLang import Get_Lang
from ..type.Bot import Bot
from ..Logger  import Log

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


class Reaction(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.Bot    = Bot
        self.client = self.Bot.Client

        self.path = '{0}/User/{1}/__Guilds__/'.format(self.Bot.Options.Path, self.Bot.Id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload) -> None:
        if payload.guild_id is None:
            return
        if payload.member.bot == True:
            return

        data_guild = Open('{0}{1}/Main.json'.format(self.path, payload.guild_id))

        guild = self.client.get_guild(payload.guild_id)
        id = payload.message_id

        if data_guild.get('Ticket', False):
            if 'Channels' in data_guild['Ticket'] and data_guild['Ticket']['Channels'] != {}:
                if str(payload.channel_id) in data_guild['Ticket']['Channels']:
                    if str(id) == data_guild['Ticket']['Channels'][str(payload.channel_id)]:
                        if str(payload.emoji.name) == "🔒":
                            await discord.utils.get(guild.channels, id=payload.channel_id).delete()
                            del data_guild['Ticket']['Channels'][str(payload.channel_id)]

                            Save('{0}{1}/Main.json'.format(self.path, guild.id), data_guild)
                            return


        if not data_guild.get('Reaction', False):
            return
        if str(id) in data_guild['Reaction']:
            if str(payload.emoji.name) in data_guild['Reaction'][str(id)]:
                
                for role in data_guild['Reaction'][str(id)][str(payload.emoji.name)]:
                    _role = discord.utils.get(guild.roles, id=role)
                    if _role is not None:
                        await payload.member.add_roles(_role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload) -> None:
        guild = self.client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if payload.guild_id is None:
            return
        if member.bot == True:
            return

        data_guild = Open('{0}{1}/Main.json'.format(self.path, payload.guild_id))

        id = payload.message_id

        if not data_guild.get('Reaction', False):
            return
        if str(id) in data_guild['Reaction']:
            if str(payload.emoji.name) in data_guild['Reaction'][str(id)]:
                for role in member.roles:
                    if role.id in data_guild["Reaction"][str(payload.message_id)][str(payload.emoji.name)]:
                        await member.remove_roles(discord.utils.get(guild.roles, id=role.id))

async def setup(Bot: Bot) -> bool:
    try:
        await Bot.Client.add_cog(Reaction(Bot))
    except Exception:
        return False
    else:
        return True