from ..GetLang          import Code, Get_User_Lang
from ..Utils            import send, Open, Save
from ..Logger           import Logger
from ..type.Bot         import Bot

_log = Logger(__name__)

import os

try:
    import discord
    from discord.ext    import commands
except ImportError:
    _log.Critical(Code('0.0.0.0.0').format(Module = 'discord'), Exit = True)
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

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
            await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.1.1'))
            return False

    @commands.Cog.listener(
        name = "on_guild_join"
    )
    async def _guild_add(self, guild: discord.Guild) -> dict:
        _log.Info(Code('0.0.0.1.2').format(guild))
        os.makedirs('{0}/{1}'.format(self._Path, guild.id), exist_ok=True)
        _log.Info(Code('0.0.0.1.3').format(server = guild.name))
        Data = Open("{0}/{1}/Main.json".format(self._Path, guild.id), {'Info':{'Members':0,'Humains':0,'Bots':0,'Name':str(guild),'Id':int(guild.id)}})

        if not 'Info' in Data:
            Data['Info'] = {'Members':0,'Humains':0,'Bots':0,'Name':str(guild),'Id':int(guild.id)}

        for Member in guild.members:
            Data["Info"]["Members"] += 1
            if not Member.bot:Data["Info"]["Humains"] += 1
            else:Data["Info"]["Bots"] += 1

        Save("{0}/{1}/Main.json".format(self._Path, guild.id), Data)
        _log.Info(Code('0.0.0.1.4').format(server = guild.name))
        return Data

    @commands.command(
        name = "verif-guild",
        aliases = [
            "Verif-guild","verif-Guild","Verif-Guild"
        ]
    )
    async def _verif_guild(self, ctx: commands.Context) -> None:
        if await self._check(ctx):
            _log.Info(Code('0.0.0.1.5'))
            for i in self.client.guilds:
                await self._guild_add(i)
            await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.1.6'))
            _log.Info(Code('0.0.0.1.6'))

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
    _cog = Join(Bot)
    try:
        _log.Info(Code('0.0.0.0.8').format(cog = _cog.__class__.__name__))
        await Bot.Client.add_cog(_cog)
    except Exception:
        _log.Warn(Code('0.0.0.0.9').format(cog = _cog.__class__.__name__))
        return False
    else:
        _log.Info(Code('0.0.0.1.0').format(cog = _cog.__class__.__name__))
        return True