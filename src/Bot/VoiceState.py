from typing      import Union
from .GetLang    import Code, Get_User_Lang
from .Logger     import Logger
from .Utils      import send
from .type.Bot   import Bot
from .YTDLSource import YTDLSource

_log = Logger(__name__)

import math
import random
import asyncio

try:
    import discord
    from discord.ext import commands
except ImportError:
    _log.Error(Code('0.0.0.0.0').format(Module = 'discord'))
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

try:
    from async_timeout import timeout
except ImportError:
    _log.Error(Code('0.0.0.0.0').format(Module = 'async_timeout'))
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

try:
    import functools
except ImportError:
    _log.Error(Code('0.0.0.0.0').format(Module = 'functools'))
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

try:
    import youtube_dl
except ImportError:
    _log.Error(Code('0.0.0.0.0').format(Module = 'youtube_dl'))
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

__all__ = (
    'VoiceState'
)

class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source    = source
        self.requester = source.requester

    def create_embed(self, user_id: int) -> discord.Embed:
        embed = discord.Embed(title = Get_User_Lang(user_id).get('0.0.2.6.6'), description = '```css\n{0}\n```'.format(self.source.title))
        embed.add_field(name = Get_User_Lang(user_id).get('0.0.2.6.7'), value = self.source.duration,   inline=False)
        embed.add_field(name = Get_User_Lang(user_id).get('0.0.2.6.8'), value = self.requester.mention, inline=False)
        embed.add_field(name = Get_User_Lang(user_id).get('0.0.2.6.9'), value = Get_User_Lang(user_id).get('0.0.2.7.0').format(name = self.source.uploader, url = self.source.uploader_url), inline=False)
        embed.add_field(name = Get_User_Lang(user_id).get('0.0.2.7.1'), value = Get_User_Lang(user_id).get('0.0.2.7.2').format(url = self.source.url), inline=False)
        embed.set_thumbnail(url = self.source.thumbnail)

        return embed

class VoiceState:
    def __init__(self, Bot: Bot, ctx: commands.Context) -> None:
        self.Bot     = Bot

        self.client  = self.Bot.Client
        self.options = self.Bot.Options
        self.ctx     = ctx

        self.voice: discord.VoiceClient = None
        self.playlist      = None
        self.video_by_name = None
        self.current       = None

        self.play          = False
        self.loop          = False

        self.volume        = 0.5


        self.ydl_opts = {
            'outtmpl':            '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'format':             'bestaudio/best',
            'source_address':     '0.0.0.0',
            'default_search':     'auto',
            'audioformat':        'mp3',
            'ignoreerrors':       False,
            'logtostderr':        False,
            'quit':               True,
            'extractaudio':       True,
            'restrictfilenames':  True,
            'playlist':           True,
            'nocheckcertificate': True,
            'quiet':              True,
            'no_warnings':        True
        }
        self.songs = []
        self.skip  = []

        self.end = ''

        self.audio_task = self.client.loop.create_task(self._audio_task())

    @property
    def is_playing(self) -> bool:
        if self.voice != None:
            return (self.voice.is_playing() == False) and (self.voice.is_paused() == False)
        return False

    async def _audio_task(self):
        index = 0
        while True:
            while (self.play == False) and (self.loop == False) and (self.is_playing == False):
                await asyncio.sleep(1)

                if self.songs == []:
                    index += 1

                if index >= 300:
                    await self.__stop()
                    index = 0

            try:
                index = 0
                if self.is_playing:
                    async with timeout(180):
                        self.current = await self._get_current()

            except asyncio.TimeoutError:
                self.client.loop.create_task(self.__stop())
                break

            except Exception as e:
                _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))

            else:
                if self.is_playing and self.current != None:
                    self.current.source.volume = self.volume
                    self.voice.play(self.current.source)

                    

                    if not self.loop:
                        await send(self.ctx, embed=self.current.create_embed(self.ctx.author.id), reference=False)
                        del self.songs[0]

                        if len(self.songs) == 0:
                            self.play = False

                await asyncio.sleep(1)

    async def _get_current(self) -> Union[Song, YTDLSource]:
        if self.loop and self.end != '':
            return Song(await YTDLSource.create_source(self.ctx, self.end, self.options, loop = self.client.loop))

        elif self.songs != []:
            self.end = self.songs[0]['url']
            return Song(await YTDLSource.create_source(self.ctx, self.songs[0]["url"], self.options, loop = self.client.loop))

        elif self.songs == []:
            self.play = False

    async def __stop(self):
        if not (self.voice == None):
            await self._leave()

        self.songs = []

    async def _join(self, ctx: commands.Context) -> bool:
        if (self.audio_task.cancelled()):
            self.audio_task = self.client.loop.create_task(self._audio_task())

        if self.voice:
            if not await self._leave():
                return False

        try:
            destination = ctx.author.voice.channel
            self.voice = await destination.connect(self_deaf=True)
            return True
        except Exception as e:
            _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
            return False

    async def _leave(self) -> bool:
        if self.is_playing:
            self.voice.stop()

        try:
            await self.voice.disconnect()
            self.voice         = None
            self.current       = 'None'
            self.play          = False
            self.loop          = False
            self.audio_task.cancel()
            return True
        except Exception as e:
            _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
            return False

    async def _play(self, ctx: commands.Context, search: str) -> None:
        if not self.voice:
            if not await self._join(ctx):
                return

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            loop = self.client.loop or asyncio.get_event_loop()

            partial = functools.partial(ydl.extract_info, search, download=False, process=False)
            data = await loop.run_in_executor(None, partial)

            if data["webpage_url_basename"] == "playlist":
                self.playlist = self.client.loop.create_task(self._playlist(ctx, data))

            elif 'title' in data:
                self.songs.append({"url": data.get('webpage_url'), "name": data.get('title')})
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.2.7.3').format(name = data.get('title')))
                if not self.play:
                    self.play = True

            else:
                with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                    partial = functools.partial(ydl.extract_info, data["url"], download=False, process=False)
                    data = await loop.run_in_executor(None, partial)

                    self.video_by_name = self.client.loop.create_task(self._video_by_name(ctx, data))

    async def _playlist(self, ctx: commands.Context, data: dict):
        n = 0
        for entrie in data.get('entries'):
            n+=1;self.songs.append({"url": "https://www.youtube.com/watch?v=" + entrie.get('url'), "name": entrie.get('title')})
        await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.2.7.4').format(list = n, name = data.get('title')))

        if not self.play:
            self.play = True

        if not (self.playlist == None):
            self.playlist.cancel()
            self.playlist = None


    async def _video_by_name(self, ctx: commands.Context, data: dict):
        n = 0
        for entrie in data.get('entries'):
            n+=1;self.songs.append({"url": "https://www.youtube.com/watch?v=" + entrie.get('url'), "name": entrie.get('title')})
        await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.2.7.3').format(name = data.get('id')))

        if not self.play:
            self.play = True

        if not (self.video_by_name == None):
            self.video_by_name.cancel()
            self.video_by_name = None

    async def _loop(self) -> bool:
        try:
            self.loop = not self.loop
            if not self.play:
                self.play = True

            return True
        except Exception as e:
            _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
            return False

    async def _stop(self):
        try:
            self.voice.stop()

            self.current       = 'None'
            self.play          = False
            self.loop          = False
            self.end           = ''

            self.songs = []

            return True
        except Exception as e:
            _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
            return False

    async def _queue(self, ctx: commands.Context, page: int):
        items = 10

        pages = math.ceil((len(self.songs) / items))

        start = (page - 1) * items
        end   = start + items

        value = ''

        for i in range(start, end):
            try:
                value += '`{0}.` [**{1}**]({2})\n'.format((i+1), self.songs[i]['name'], self.songs[i]['url'])
            except IndexError:
                break

        embed = discord.Embed(description = '**{0} {1}**\n\n{2}'.format(len(self.songs), Get_User_Lang(ctx.author.id).get('0.0.0.4.4'), value))
        embed.set_footer(text=Get_User_Lang(ctx.author.id).get('0.0.0.2.9').format(page = page, pages = pages))

        await send(ctx, embed = embed)


    async def _skip(self, ctx: commands.Context):
            voter = ctx.author

            if voter == self.current.requester:
                await ctx.message.add_reaction('⏭')
                self.loop = False
                self.voice.stop()
                return True

            elif str(voter.id) not in self.skip:
                self.skip.append(str(voter.id))
                total = len(self.skip)

                if total >= 3:
                    self.skip = []
                    await ctx.message.add_reaction('⏭')
                    self.loop = False
                    self.voice.stop()
                    return True

                else:
                    await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.2.7.6').format(total = total))

            else:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.2.7.7'))

    async def _volume(self, ctx: commands.Context, volume: Union[float, bool]):
        if volume == False:
            await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.2.7.8').format(volume = (self.volume*100)))

        elif 0 > volume or volume > 100:
            await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.2.7.9'))

        else:
            self.volume = volume/100
            await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.2.8.0').format(volume = volume))

    async def _pause(self):
        try:
            self.voice.pause()
            return True
        except Exception as e:
            _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
            return False

    async def _resume(self):
        try:
            if self.voice.is_paused():
                self.voice.resume()
            return True
        except Exception as e:
            _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
            return False

    async def _shuffle(self):
        try:
            random.shuffle(self.songs)
            return True
        except Exception as e:
            _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
            return False

    async def _remove(self, ctx: commands.Context, index: int):
        def reaction_check(reaction, user: discord.Member):
            return user == ctx.author and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌') and (reaction.message.id == message.id)
        
        music = self.songs[index-1]
        message = await send(ctx, embed = discord.Embed(description = Get_User_Lang(ctx.author.id).get('0.0.2.8.1').format(name = music['name'], url = music['url'])))

        await message.add_reaction('✅')
        await message.add_reaction('❌')

        try:
            reaction, user = await self.client.wait_for('reaction_add', check = reaction_check, timeout = 300)
        except asyncio.TimeoutError:
            await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.2.8.2'))
        except Exception as e:
            _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
        else:
            await message.clear_reactions()

            if str(reaction.emoji) == '✅':
                del self.songs[index-1]
                await message.edit(embed = discord.Embed(description = Get_User_Lang(ctx.author.id).get('0.0.2.8.3').format(name = music['name'])))
            else:
                await message.delete()