from ..GetLang          import Code, Get_User_Lang
from ..Utils            import send, Open, Save
from ..Logger           import Logger
from ..type.Bot         import Bot

_log = Logger(__name__)

import asyncio
from   typing           import Union

try:
    import discord
    from discord.ext    import commands
except ImportError:
    _log.Critical(Code('0.0.0.0.0').format(Module = 'discord'), Exit = True)
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

class Reactions(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.Bot    = Bot
        self.client = self.Bot.Client

        self.path = '{0}/User/{1}/__Guilds__/'.format(self.Bot.Options.Path, self.Bot.Id)

    async def _check(self, ctx: commands.Context) -> bool:
        if ctx.author.bot == False:
            if not (ctx.guild):
                await send(ctx, message =  Get_User_Lang(ctx.author.id).get("0.0.0.2.2"))
                return False
            else:
                if ctx.author.guild_permissions.manage_roles:
                    return True
                else:
                    await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.1.1"))
                    return False

    @commands.command(
        name = "Add-role-reac",
        aliases = [
            "Add-Role-reac",
            "Add-Role-Reac",
            "add-Role-Reac",
            "add-role-Reac",
            "add-role-reac"
        ]
    )
    async def add_role_reac(self, ctx: commands.Context) -> None:
        if await self._check(ctx):
            embed = await self._get_info(ctx)

            self.client.loop.create_task(self._add_reactions(ctx, embed))


    async def _get_info(self, ctx: commands.Context) -> Union[discord.Embed, discord.Message]:
        def reaction_check(reaction, user: discord.Member):
            return user == ctx.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌') and (reaction.message.id == message.id)

        def message_check(_message: discord.Message):
            return _message.author == ctx.author and _message.channel == ctx.channel

        title = ''
        description = ''

        message = await send(ctx, embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.0.7.9")))

        await message.add_reaction('✅')
        await message.add_reaction('❌')

        try:
            reaction, user = await self.client.wait_for('reaction_add', check = reaction_check, timeout = 300)
        except asyncio.TimeoutError:
            await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.3.8'))
        except Exception as e:
            _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
        else:
            await message.clear_reactions()

            if str(reaction.emoji) == '✅':
                await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.8.0")))

                try:
                    reponse = await self.client.wait_for('message', check = message_check, timeout = 300)
                except asyncio.TimeoutError:
                    await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.3.8'))
                except Exception as e:
                    _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
                else:
                    title = reponse.content
                    await reponse.delete()
            else:
                await message.clear_reactions()

        await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.0.8.1")))

        await message.add_reaction('✅')
        await message.add_reaction('❌')

        try:
            reaction, user = await self.client.wait_for('reaction_add', check = reaction_check, timeout = 300)
        except asyncio.TimeoutError:
            await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.3.8'))
        except Exception as e:
            _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
        else:
            await message.clear_reactions()

            if str(reaction.emoji) == '✅':
                await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.0.8.2")))

                try:
                    reponse = await self.client.wait_for('message', check = message_check, timeout = 300)
                except asyncio.TimeoutError:
                    await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.3.8'))
                except Exception as e:
                    _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
                else:
                    description = reponse.content
                    await reponse.delete()
            else:
                await message.clear_reactions()

        await message.delete()
        embed = discord.Embed()

        if title != '':
            embed.title = title
        if description != '':
            embed.description = description

        return await send(ctx, embed = embed, reference=False)


    async def _add_reactions(self, ctx: commands.Context, _message: Union[discord.Embed, discord.Message]) -> None:
        def reaction_check(reaction, user: discord.Member):
            return user == ctx.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌') and (reaction.message.id == message.id)

        def message_reaction_check(reaction, user: discord.Member):
            return user == ctx.author and (reaction.message.id == message.id)

        def message_check(_message: discord.Message):
            return _message.author == ctx.author and _message.channel == ctx.channel

        message = await send(ctx, embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.0.8.3")))
        while True:
            if len(_message.reactions) == 19:
                await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.0.8.4")))
                break

            await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.0.8.5")))

            try:
                reaction, user = await self.client.wait_for('reaction_add', check = message_reaction_check, timeout = 300)
            except asyncio.TimeoutError:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.3.8'))
                break
            except Exception as e:
                _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
                break

            _reaction = reaction.emoji
            await _message.add_reaction(_reaction)

            await message.clear_reactions()

            await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.0.8.6")))

            try:
                reponse = await self.client.wait_for('message', check = message_check, timeout = 300)
            except asyncio.TimeoutError:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.3.8'))
                break
            except Exception as e:
                _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
                break

            _role = reponse.content[3:-1]
            await reponse.delete()

            guild_data = Open('{0}{1}/Main.json'.format(self.path, ctx.guild.id))

            if not 'Reaction' in guild_data:
                guild_data['Reaction'] = {str(_message.id): {str(_reaction): [int(_role)]}}

            if not str(_message.id) in guild_data['Reaction']:
                guild_data['Reaction'][str(_message.id)] = {str(_reaction): [int(_role)]}

            if not str(_reaction) in guild_data['Reaction'][str(_message.id)]:
                guild_data['Reaction'][str(_message.id)][str(_reaction)] = [int(_role)]

            if not int(_role) in guild_data['Reaction'][str(_message.id)][str(_reaction)]:
                guild_data['Reaction'][str(_message.id)][str(_reaction)].append(int(_role))

            Save('{0}{1}/Main.json'.format(self.path, ctx.guild.id), guild_data)

            await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.0.8.7")))

            await message.add_reaction('✅')
            await message.add_reaction('❌')

            try:
                reaction, user = await self.client.wait_for('reaction_add', check = reaction_check, timeout = 300)
            except asyncio.TimeoutError:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.3.8'))
                break
            except Exception as e:
                _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
                break
            else:
                await message.clear_reactions()

                if str(reaction.emoji) == '❌':
                    await message.delete()
                    break


    @commands.command(
        name = "Edit-role-reac",
        aliases = [
            "Edit-Role-reac",
            "Edit-Role-Reac",
            "edit-Role-Reac",
            "edit-role-Reac",
            "edit-role-reac"
        ]
    )
    async def edit_role_reac(self, ctx: commands.Context, id: int = False) -> None:
        if await self._check(ctx):
            if id:
                message = await ctx.fetch_message(id)
            elif ctx.message.reference:
                message = await ctx.fetch_message(ctx.message.reference.message_id)
            else:
                await send(ctx, embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.0.8.8"), description = Get_User_Lang(ctx.author.id).get("0.0.0.8.9")))
                return
            self.client.loop.create_task(self._add_reactions(ctx, message))

async def setup(Bot: Bot) -> bool:
    _cog = Reactions(Bot)
    try:
        _log.Info(Code('0.0.0.0.8').format(cog = _cog.__class__.__name__))
        await Bot.Client.add_cog(_cog)
    except Exception:
        _log.Warn(Code('0.0.0.0.9').format(cog = _cog.__class__.__name__))
        return False
    else:
        _log.Info(Code('0.0.0.1.0').format(cog = _cog.__class__.__name__))
        return True