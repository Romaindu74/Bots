from ..GetLang          import Code, Get_User_Lang
from ..Utils            import send, Open, Save
from ..Logger           import Logger
from ..type.Bot         import Bot

_log = Logger(__name__)

import math
import asyncio

try:
    import discord
    from discord.ext    import commands
except ImportError:
    _log.Critical(Code('0.0.0.0.0').format(Module = 'discord'), Exit = True)
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

class Status(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.Bot    = Bot

        self.client = self.Bot.Client

        self.path = '{0}/User/Bots/{1}/'.format(self.Bot.Options.Path, self.Bot.Id)

    async def _check(self, ctx: commands.Context) -> None:
        if str(ctx.author.id) in self.Bot.Info.get('Owner', []):
            return True
        elif not ctx.author.bot:
            await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.1.1'))
            return False

    @commands.command(
        name = "new-status",
        aliases = [
            "New-status", 'nEw-status', 'neW-status',
            'new-Status', 'new-sTatus', 'new-stAtus',
            'new-staTus', 'new-statUs', 'new-statuS'
        ])
    async def _new_statu(self, ctx: commands.Context) -> None:
        if await self._check(ctx):
            def reaction_check(reaction, user: discord.Member):
                return user == ctx.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌') and (reaction.message.id == message.id)

            def message_check(_message: discord.Message):
                return _message.author == ctx.author and _message.channel == ctx.channel

            message = await send(ctx, embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.0.3.6").format(user = ctx.author), description = Get_User_Lang(ctx.author.id).get('0.0.0.3.7')))

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

                if str(reaction.emoji) == '❌':
                    return
                if str(reaction.emoji) == '✅':
                    await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get('0.0.0.3.9'), description = Get_User_Lang(ctx.author.id).get('0.0.0.4.0')))
                    
                    try:
                        reponse = await self.client.wait_for('message', check = message_check, timeout = 300)
                    except asyncio.TimeoutError:
                        await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.3.8'))
                        return
                    except Exception as e:
                        _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
                        return
                    else:
                        try:
                            type = int(reponse.content)
                        except ValueError:
                            await message.delete()
                            return
                        await reponse.delete()

                    await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get('0.0.0.4.1'), description = Get_User_Lang(ctx.author.id).get('0.0.0.4.2')))

                    try:
                        reponse = await self.client.wait_for('message', check = message_check, timeout = 300)
                    except asyncio.TimeoutError:
                        await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.3.8'))
                        return
                    except Exception as e:
                        _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
                        return
                    else:
                        _statu = str(reponse.content)
                        if not (_statu == 'online' or _statu == 'offline' or _statu == 'idle' or _statu == 'dnd' or _statu == 'invisible'):
                            await message.delete()
                            return
                        await reponse.delete()

                    await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get('0.0.0.4.3')))

                    try:
                        reponse = await self.client.wait_for('message', check = message_check, timeout = 300)
                    except asyncio.TimeoutError:
                        await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.3.8'))
                        return
                    except Exception as e:
                        _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
                        return
                    else:
                        try:
                            sleep = int(reponse.content)
                        except ValueError:
                            await message.delete()
                            return

                    await reponse.delete()
                    await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get('0.0.0.4.4')))

                    try:
                        reponse = await self.client.wait_for('message', check = message_check, timeout = 300)
                    except asyncio.TimeoutError:
                        await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.3.8'))
                        return
                    except Exception as e:
                        _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
                        return
                    else:
                        text = str(reponse.content)
                        await reponse.delete()

                    status = Open("{0}/Status.json".format(self.path), {"Status": []})

                    if not status.get('Status', False):
                        status["Status"] = []

                    status["Status"].append({"Type": type, "Status": _statu, "Text": text, "Sleep": sleep})

                    Save("{0}/Status.json".format(self.path), status)

                    await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.0.4.5")))

    @commands.command(
        name = "view-status",
        aliases = [
            "View-status", 'vIew-status', 'viEw-status', 'vieW-status'
            'view-Status', 'view-sTatus', 'view-stAtus',
            'view-staTus', 'view-statUs', 'view-statuS'
        ])
    async def _view_status(self, ctx: commands.Context, page: int = 1) -> None:
        if await self._check(ctx):
            status = Open("{0}/Status.json".format(self.path), {"Status": []})

            if not status.get('Status', False):
                status["Status"] = []

            if status["Status"] != []:
                items_per_page = 10
                pages = math.ceil(len(status["Status"]) / items_per_page)
                start = (page - 1) * items_per_page
                end = start + items_per_page
                embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.0.4.6"), color=ctx.author.color)

                for i in range(start, end):
                    try:
                        embed.add_field(name = f"({i+1})", value = "\"**{Value}**\": \"**{0}**\"\n\"**{Sleep}**\": \"**{1}**\"\n\"**{Status}**\": \"**{2}**\"\n\"**{Type}**\": \"**{3}**\"".format(
                            status["Status"][i]["Text"],
                            status["Status"][i]["Sleep"],
                            status["Status"][i]["Status"],
                            status["Status"][i]["Type"],
                            Value =  Get_User_Lang(ctx.author.id).get("0.0.0.4.7"),
                            Sleep =  Get_User_Lang(ctx.author.id).get("0.0.0.4.8"),
                            Status = Get_User_Lang(ctx.author.id).get("0.0.0.4.9"),
                            Type =   Get_User_Lang(ctx.author.id).get("0.0.0.5.0")
                        ),inline = False)
                    except IndexError:
                        pass
                embed.set_footer(text = Get_User_Lang(ctx.author.id).get("0.0.0.2.9").format(page = page, pages = pages))
                await send(ctx, embed=embed)
            else:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.5.1"))


    @commands.command(
        name = "remove-status",
        aliases = [
            "Remove-status", 'rEmove-status', 'reMove-status', 'remOve-status', 'remoVe-status', 'removE-status'
            'remove-Status', 'remove-sTatus', 'remove-stAtus',
            'remove-staTus', 'remove-statUs', 'remove-statuS'
        ])
    async def _remove_status(self, ctx: commands.Context, page: int = 1) -> None:
        if await self._check(ctx):
            def reaction_check(reaction, user: discord.Member):
                return user == ctx.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌') and (reaction.message.id == message.id)

            def message_check(_message: discord.Message):
                return _message.author == ctx.author and _message.channel == ctx.channel

            message = await send(ctx, embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get('0.0.0.3.6').format(user = ctx.author), description = Get_User_Lang(ctx.author.id).get('0.0.0.5.2')))

            await message.add_reaction('✅')
            await message.add_reaction('❌')

            try:
                reaction, user = await self.client.wait_for('reaction_add', check = reaction_check, timeout = 300)
            except asyncio.TimeoutError:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.3.8'))
                return
            except Exception as e:
                _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
                return

            await message.clear_reactions()

            if str(reaction.emoji) == '❌':
                return
            if str(reaction.emoji) == '✅':
                status = Open("{0}/Status.json".format(self.path), {"Status": []})

                if not status.get('Status', False):
                    status["Status"] = []

                if status["Status"] != []:
                    items_per_page = 10
                    pages = math.ceil(len(status["Status"]) / items_per_page)
                    start = (page - 1) * items_per_page
                    end = start + items_per_page
                    embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get("0.0.0.4.6"), color=ctx.author.color)

                    for i in range(start, end):
                        try:
                            embed.add_field(name = f"({i+1})", value = "\"**{Value}**\": \"**{0}**\"\n\"**{Sleep}**\": \"**{1}**\"\n\"**{Status}**\": \"**{2}**\"\n\"**{Type}**\": \"**{3}**\"".format(
                                status["Status"][i]["Text"],
                                status["Status"][i]["Sleep"],
                                status["Status"][i]["Status"],
                                status["Status"][i]["Type"],
                                Value =  Get_User_Lang(ctx.author.id).get("0.0.0.4.7"),
                                Sleep =  Get_User_Lang(ctx.author.id).get("0.0.0.4.8"),
                                Status = Get_User_Lang(ctx.author.id).get("0.0.0.4.9"),
                                Type =   Get_User_Lang(ctx.author.id).get("0.0.0.5.0")
                            ),inline = False)
                        except IndexError:
                            pass
                    embed.add_field(name = Get_User_Lang(ctx.author.id).get("0.0.0.5.3"), value = Get_User_Lang(ctx.author.id).get("0.0.0.5.4"))
                    embed.set_footer(text = Get_User_Lang(ctx.author.id).get("0.0.0.2.9").format(page = page, pages = pages))
                    await message.edit(embed=embed)
                    try:
                        reponse = await self.client.wait_for("message", check = message_check, timeout = 300)
                    except asyncio.TimeoutError:
                        await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.3.8'))
                        return
                    except Exception as e:
                        _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
                        return
                    await reponse.delete()
                    try:
                        num = int(reponse.content)
                    except ValueError:
                        await message.delete()
                        return

                    if len(status['Status']) < num:
                        await message.delete()
                        return

                    del status["Status"][num-1]
                    Save("{0}/Status.json".format(self.path), status)
                    await message.edit(embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get('0.0.0.5.5')))
                else:
                    await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.5.1"))

async def setup(Bot: Bot) -> bool:
    _cog = Status(Bot)
    try:
        _log.Info(Code('0.0.0.0.8').format(cog = _cog.__class__.__name__))
        await Bot.Client.add_cog(_cog)
    except Exception:
        _log.Warn(Code('0.0.0.0.9').format(cog = _cog.__class__.__name__))
        return False
    else:
        _log.Info(Code('0.0.0.1.0').format(cog = _cog.__class__.__name__))
        return True