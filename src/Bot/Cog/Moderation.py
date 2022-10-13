from datetime import datetime
from typing   import Union
from time     import monotonic

from ..GetLang  import Get_Lang
from ..type.Bot import Bot
from ..Logger   import Log
from ..Utils    import MISSING, send, Save, Open

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

class Moderations(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.Bot = Bot

    def _check(self, ctx: commands.Context) -> bool:
        return ctx.author.bot == False

    @commands.command(
        name = 'ban',
        aliases = [
            'Ban', 'bAn', 'baN',
            'BAn', 'bAN', 'BaN',
            'BAN'
        ]
    )
    async def _ban(self, ctx: commands.Context, member: Union[int, discord.Member, discord.User] = MISSING, *, raison = None) -> None:
        if self._check(ctx):
            if member is MISSING:
                await send(ctx, message = 'Tu n\'a pas mentionner le membre en question')
                return

            if not ctx.bot_permissions.ban_members:
                await send(ctx, message= 'Le bot n\'a pas la permition de faire cela')
                return
            
            if not ctx.author.guild_permissions.ban_members:
                await send(ctx, message = 'Tu n\'a pas la permition de faire cela')
                return

            if isinstance(member, int):
                class Id:
                    id: int   = member
                    name: str = str(member)
                member = Id()

            try:
                await ctx.guild.ban(member, reason = raison)
            except discord.Forbidden:
                await send(ctx, message = 'Je n\'ai pas reussi a bannir ce membre', reference=False)
            else:
                await send(ctx, embed=discord.Embed(title = '{0} a été Banni du serveur'.format(member.name), timestamp = datetime.now()))

    @commands.command(
        name = 'unban',
        aliases = [
            'Unban', 'uNban', 'unBan',
            'unbAn', 'unbaN'
        ]
    )
    async def _unban(self, ctx: commands.Context, member: Union[int, discord.Member, discord.User] = MISSING, *, raison = None) -> None:
        if self._check(ctx):
            if member is MISSING:
                await send(ctx, message = 'Tu n\'a pas mentionner le membre en question')
                return

            if not ctx.bot_permissions.ban_members:
                await send(ctx, message= 'Le bot n\'a pas la permition de faire cela')
                return
            
            if not ctx.author.guild_permissions.ban_members:
                await send(ctx, message = 'Tu n\'a pas la permition de faire cela')
                return

            if isinstance(member, int):
                class Id:
                    id: int   = member
                    name: str = str(member)
                member = Id()

            try:
                await ctx.guild.unban(member, reason=raison)
            except discord.Forbidden:
                await send(ctx, message = 'Je n\'ai pas reussi a bannir ce membre', reference=False)
            except discord.NotFound:
                await send(ctx, message = 'Ce membre n\'es pas banni', reference=False)
            else:
                await send(ctx, embed=discord.Embed(title = '{0} n\'est plus banni du serveur'.format(member.name), timestamp = datetime.now()))


    @commands.command(
        name = 'kick',
        aliases = [
            'Kick', 'kIck', 'kiCk', 'kicK',
            'KIck', 'kICk', 'kiCK', 'KicK',
            'KICk', 'kICK', 'KiCK', 'KIcK',
            'KICK'
        ]
    )
    async def _kick(self, ctx: commands.Context, member: Union[int, discord.Member] = MISSING, *, raison = None) -> None:
        if self._check(ctx):
            if member is MISSING:
                await send(ctx, message = 'Tu n\'a pas mentionner le membre en question')
                return

            if not ctx.bot_permissions.kick_members:
                await send(ctx, message= 'Le bot n\'a pas la permition de faire cela')
                return
            
            if not ctx.author.guild_permissions.kick_members:
                await send(ctx, message = 'Tu n\'a pas la permition de faire cela')
                return

            if isinstance(member, int):
                member = ctx.guild.get_member(member)

            try:
                await member.kick(reason = raison)
            except discord.Forbidden:
                await send(ctx, message = 'Je n\'ai pas reussi a expulser ce membre', reference=False)
            else:
                await send(ctx, embed=discord.Embed(title = '{0} a été expulser du serveur'.format(member.name), timestamp = datetime.now()))


    @commands.command(
        name = 'mute',
        aliases = [
            'Mute', 'mUte', 'muTe', 'mutE',
            'MUte', 'mUTe', 'muTE', 'MutE',
            'MUTe', 'mUTE', 'MuTE', 'MUtE',
            'MUTE'
        ]
    )
    async def _mute(self, ctx: commands.Context, member: Union[int, discord.Member] = MISSING, *, raison = None) -> None:
        if self._check(ctx):
            if member is MISSING:
                await send(ctx, message = 'Tu n\'a pas mentionner le membre en question')
                return

            if not ctx.bot_permissions.manage_roles or not ctx.bot_permissions.manage_channels:
                await send(ctx, message= 'Le bot n\'a pas la permition de faire cela')
                return
            
            if not ctx.author.guild_permissions.manage_roles or not ctx.bot_permissions.manage_channels:
                await send(ctx, message = 'Tu n\'a pas la permition de faire cela')
                return

            if isinstance(member, int):
                member = ctx.guild.get_member(member)

            if not 'Mute' in ([r.name for r in ctx.guild.roles]):
                Role = await ctx.guild.create_role(reason = 'For Mute Users', name = 'Mute')
                await Role.edit(permissions=discord.Permissions(read_messages = True, send_messages = False))

                for channel in ctx.guild.channels:
                    await channel.set_permissions(Role, overwrite = discord.PermissionOverwrite(read_messages = True, send_messages = False))

            else:
                Role = discord.utils.get(ctx.guild.roles, name = 'Mute')

            try:
                await member.add_roles(Role)
            except discord.Forbidden:
                await send(ctx, message = 'Je n\'ai pas reussi a mute ce membre', reference=False)
            else:
                await send(ctx, embed=discord.Embed(title = '{0} a été mute du serveur'.format(member.name), timestamp = datetime.now()))

    @commands.command(
        name = 'tempmute',
        aliases = [
            'Tempmute', 'TempMute', 'TEMPMUTE'
        ]
    )
    async def _tempmute(self, ctx: commands.Context, member: Union[int, discord.Member] = MISSING, temp: int = MISSING, *, raison = None) -> None:
        if self._check(ctx):
            if member is MISSING:
                await send(ctx, message = 'Tu n\'a pas mentionner le membre en question')
                return

            if temp is MISSING:
                await send(ctx, message = 'Tu n\'a pas donner un temp limite')
                return

            if not ctx.bot_permissions.manage_roles or not ctx.bot_permissions.manage_channels:
                await send(ctx, message= 'Le bot n\'a pas la permition de faire cela')
                return
            
            if not ctx.author.guild_permissions.manage_roles or not ctx.bot_permissions.manage_channels:
                await send(ctx, message = 'Tu n\'a pas la permition de faire cela')
                return

            if isinstance(member, int):
                member = ctx.guild.get_member(member)

            if not 'Mute' in ([r.name for r in ctx.guild.roles]):
                Role = await ctx.guild.create_role(reason = 'For Mute Users', name = 'Mute')
                await Role.edit(permissions=discord.Permissions(read_messages = True, send_messages = False))

                for channel in ctx.guild.channels:
                    await channel.set_permissions(Role, overwrite = discord.PermissionOverwrite(read_messages = True, send_messages = False))

            else:
                Role = discord.utils.get(ctx.guild.roles, name = 'Mute')

            try:
                await member.add_roles(Role)
                guild = Open('{0}/User/{1}/__Guilds__/{2}/Main.json'.format(self.Bot.Options.Path, self.Bot.Id, ctx.guild.id))
                if not 'Temps-Mute' in guild:
                    guild['Temps-Mute'] = {}
                guild['Temps-Mute'][str(member.id)] = int(monotonic())+temp
                Save('{0}/User/{1}/__Guilds__/{2}/Main.json'.format(self.Bot.Options.Path, self.Bot.Id, ctx.guild.id), guild)
            except discord.Forbidden:
                await send(ctx, message = 'Je n\'ai pas reussi a mute ce membre', reference=False)
            else:
                await send(ctx, embed=discord.Embed(title = '{0} a été mute du serveur pandant {1}s'.format(member.name, temp), timestamp = datetime.now()))



async def setup(Bot: Bot) -> bool:
    try:
        await Bot.Client.add_cog(Moderations(Bot))
    except Exception:
        return False
    else:
        return True