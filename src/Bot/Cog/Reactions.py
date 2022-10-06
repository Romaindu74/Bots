from typing import Union
from ..GetLang import Get_Lang, Get_User_Lang
from ..type.Bot import Bot
from ..Logger  import Log
from ..Utils   import send, Open, Save

try:
    import asyncio
except ImportError:
    Log(50, Get_Lang.get('0.0.0.0.0').format(Name = 'asyncio'), True)
except Exception as e:
    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)

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


class Reactions(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.Bot    = Bot
        self.client = self.Bot.Client

        self.path = '{0}/User/{1}/__Guilds__/'.format(self.Bot.Options.Path, self.Bot.Id)

    async def _check(self, ctx: commands.Context) -> bool:
        if ctx.author.bot == False:
            if not (ctx.guild):
                await send(ctx, message =  Get_User_Lang(ctx.author.id).get("0.0.0.9.3"))
                return False
            else:
                if ctx.author.guild_permissions.manage_roles:
                    return True
                else:
                    await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.8.0"))
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

        message = await send(ctx, embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.1.0.7")))

        await message.add_reaction('✅')
        await message.add_reaction('❌')

        try:
            reaction, user = await self.client.wait_for('reaction_add', check = reaction_check, timeout = 300)
        except asyncio.TimeoutError:
            await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.5.2'))
        except Exception as e:
            Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)))
        else:
            await message.clear_reactions()

            if str(reaction.emoji) == '✅':
                await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.1.0.8")))

                try:
                    reponse = await self.client.wait_for('message', check = message_check, timeout = 300)
                except asyncio.TimeoutError:
                    await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.5.2'))
                except Exception as e:
                    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)))
                else:
                    title = reponse.content
                    await reponse.delete()
            else:
                await message.clear_reactions()

        await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.1.0.9")))

        await message.add_reaction('✅')
        await message.add_reaction('❌')

        try:
            reaction, user = await self.client.wait_for('reaction_add', check = reaction_check, timeout = 300)
        except asyncio.TimeoutError:
            await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.5.2'))
        except Exception as e:
            Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)))
        else:
            await message.clear_reactions()

            if str(reaction.emoji) == '✅':
                await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.1.1.0")))

                try:
                    reponse = await self.client.wait_for('message', check = message_check, timeout = 300)
                except asyncio.TimeoutError:
                    await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.5.2'))
                except Exception as e:
                    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)))
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

        message = await send(ctx, embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.1.1.1")))
        while True:
            if len(_message.reactions) == 19:
                await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.1.1.2")))
                break

            await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.1.1.3")))

            try:
                reaction, user = await self.client.wait_for('reaction_add', check = message_reaction_check, timeout = 300)
            except asyncio.TimeoutError:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.5.2'))
                break
            except Exception as e:
                Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)))
                break

            _reaction = reaction.emoji
            await _message.add_reaction(_reaction)

            await message.clear_reactions()

            await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.1.1.4")))

            try:
                reponse = await self.client.wait_for('message', check = message_check, timeout = 300)
            except asyncio.TimeoutError:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.5.2'))
                break
            except Exception as e:
                Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)))
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

            await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.1.1.5")))

            await message.add_reaction('✅')
            await message.add_reaction('❌')

            try:
                reaction, user = await self.client.wait_for('reaction_add', check = reaction_check, timeout = 300)
            except asyncio.TimeoutError:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.5.2'))
                break
            except Exception as e:
                Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)))
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
                await send(ctx, embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.1.1.6"), description = Get_User_Lang(ctx.author.id).get("0.0.1.1.7")))
                return
            self.client.loop.create_task(self._add_reactions(ctx, message))

async def setup(Bot: Bot):
    try:
        await Bot.Client.add_cog(Reactions(Bot))
    except Exception:
        return False
    else:
        return True