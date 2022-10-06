from ..GetLang  import Get_Lang, Get_User_Lang
from ..type.Bot import Bot
from ..Logger   import Log
from ..Utils    import send, Open, Save

import os

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

class Join(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.Bot              = Bot
        self.client           = self.Bot.Client
        self.options          = self.Bot.Options

        self._Path = '{0}/User/{1}/__Guilds__'.format(self.options.Path, self.Bot.Id)

    async def _check(self, ctx: commands.Context) -> bool:
        if str(ctx.author.id) in self.Bot.Info.get('Owner', []):
            return True
        elif not ctx.author.bot:
            await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.8.0'))
            return False

    @commands.Cog.listener(
        name = "on_guild_join"
    )
    async def _guild_add(self, guild: discord.Guild) -> None:
        os.makedirs('{0}/{1}'.format(self._Path, guild.id), exist_ok=True)
        Data = Open("{0}/{1}/Main.json".format(self._Path, guild.id), {'Info':{'Members':0,'Humains':0,'Bots':0,'Name':str(guild),'Id':int(guild.id)}})

        if not 'Info' in Data:
            Data['Info'] = {'Members':0,'Humains':0,'Bots':0,'Name':str(guild),'Id':int(guild.id)}

        for Member in guild.members:
            Data["Info"]["Members"] += 1
            if not Member.bot:Data["Info"]["Humains"] += 1
            else:Data["Info"]["Bots"] += 1

        Save("{0}/{1}/Main.json".format(self._Path, guild.id), Data)
        return Data

    @commands.command(
        name = "verif-guild",
        aliases = [
            "Verif-guild","verif-Guild","Verif-Guild"
        ]
    )
    async def _verif_guild(self, ctx: commands.Context) -> None:
        if await self._check(ctx):
            Log(20, Get_User_Lang(ctx.author.id).get('0.0.0.8.1'))
            for i in self.client.guilds:
                await self._guild_add(i)
            await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.8.2'))
            Log(20, Get_User_Lang(ctx.author.id).get('0.0.0.8.3'))

    @commands.Cog.listener(
        name = "on_member_join"
    )
    async def _member_add(self, member: discord.Member) -> None:
        os.makedirs('{0}/{1}'.format(self._Path, member.guild.id), exist_ok=True)
        Data = Open("{0}/{1}/Main.json".format(self._Path, member.guild.id), {'Info':{'Members':0,'Humains':0,'Bots':0,'Name':str(member.guild),'Id':int(member.guild.id)}})

        if not 'Info' in Data:
            Data = await self._guild_add(member.guild)

        Data["Info"]["Members"] += 1
        if not member.bot:Data["Info"]["Humains"] += 1
        else:             Data["Info"]["Bots"] += 1

        Save("{0}/{1}/Main.json".format(self._Path, member.guild.id), Data)

    @commands.Cog.listener(
        name = "on_member_leave"
    )
    async def _member_leave(self, member: discord.Member) -> None:
        os.makedirs('{0}/{1}'.format(self._Path, member.guild.id), exist_ok=True)
        Data = Open("{0}/{1}/Main.json".format(self._Path, member.guild.id), {'Info':{'Members':0,'Humains':0,'Bots':0,'Name':str(member.guild),'Id':int(member.guild.id)}})

        if not 'Info' in Data:
            Data = await self._guild_add(member.guild)

        Data["Info"]["Members"] -= 1
        if not member.bot:Data["Info"]["Humains"] -= 1
        else:             Data["Info"]["Bots"] -= 1

        Save("{0}/{1}/Main.json".format(self._Path, member.guild.id), Data)

async def setup(Bot: Bot) -> bool:
    try:
        await Bot.Client.add_cog(Join(Bot))
    except Exception:
        return False
    else:
        return True