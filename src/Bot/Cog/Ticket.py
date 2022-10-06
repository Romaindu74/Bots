from ..GetLang import Get_Lang, Get_User_Lang
from ..type.Bot import Bot
from ..Logger  import Log
from ..Utils    import send, channel_send, Open, Save

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

class Ticket(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.Bot    = Bot
        self.client = self.Bot.Client

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
        name = 'ticket',
        aliases = [
            'Ticket', 'tIcket', 'tiCket', 'ticKet', 'tickEt', 'tickeT'
        ]
    )
    async def _ticket(self, ctx: commands.Context) -> None:
        if await self._check(ctx):
            guild_data = Open('{0}{1}/Main.json'.format(self.path, ctx.guild.id))

            if not guild_data.get('Ticket', False):
                guild_data['Ticket'] = {'Channels': {}}

            if not guild_data['Ticket'].get('Channels', False):
                guild_data['Ticket']['Channels'] = {}

            Guild: discord.Guild                             = ctx.guild
            _Ticket:      dict                               = guild_data.get('Ticket')
            index:        int                                = len(_Ticket.get('Channels'))
            _Category_id: int                                = _Ticket.get('Category', None)
            _Category:    discord.CategoryChannel            = discord.utils.get(Guild.categories, id = _Category_id) if _Category_id is not None else None
            _Admins:      list                               = _Ticket.get('Admins', [])

            _Overwrites = {
                Guild.default_role:  discord.PermissionOverwrite(view_channel=False),
                ctx.author:          discord.PermissionOverwrite(view_channel=True)
            }

            for id in _Admins:
                _Admin = Guild.get_member(id)
                if id in Guild.members and _Admins is not None:
                    _Overwrites[_Admin] = discord.PermissionOverwrite(view_channel=False)

                else:
                    _Role = discord.utils.get(Guild.roles, id=id)
                    if _Role is not None:
                        _Overwrites[_Role] = discord.PermissionOverwrite(view_channel=False)

            while True:
                if (discord.utils.get(Guild.channels, name='ticket-{0}'.format(index))) is None:
                    _Channel = await Guild.create_text_channel('ticket-{0}'.format(index),
                        overwrites=_Overwrites,
                        category  =_Category
                    )
                    _Message = await channel_send(_Channel, embed=discord.Embed(description=Get_User_Lang(ctx.author.id).get('0.0.1.3.5')))
                    await _Message.add_reaction('🔒')
                    break
                else:
                    index += 1

            guild_data['Ticket']['Channels'][str(_Channel.id)] = str(_Message.id)

            Save('{0}{1}/Main.json'.format(self.path, ctx.guild.id), guild_data)

async def setup(Bot: Bot) -> bool:
    try:
        await Bot.Client.add_cog(Ticket(Bot))
    except Exception:
        return False
    else:
        return True