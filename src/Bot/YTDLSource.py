from .GetLang import Get_Lang, Get_User_Lang
from .Logger  import Log
from .Utils   import send
from .type.Options import Options

try:
    import discord
    from discord.ext import commands
except ImportError:
    Log(50, Get_Lang.get('0.0.0.0.0').format(Name = 'discord'), True)
except Exception as e:
    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)

import asyncio
import functools

try:
    import youtube_dl
except ImportError:
    Log(50, Get_Lang.get('0.0.0.0.0').format(Name = 'youtube_dl'), True)
except Exception as e:
    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)

youtube_dl.utils.bug_reports_message = lambda: ''

class YTDLError(Exception):
    pass

class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'playlist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')), self.requester.id)
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, options: Options, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            await send(ctx, Get_User_Lang(ctx.author.id).get('0.0.0.5.4').format(Search = search), reference=False)
            return None

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                await send(ctx, Get_User_Lang(ctx.author.id).get('0.0.0.5.4').format(Search = search), reference=False)
                return None

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            await send(ctx, Get_User_Lang(ctx.author.id).get('0.0.0.5.5').format(Webpage_url = webpage_url), reference=False)
            return None

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    await send(ctx, Get_User_Lang(ctx.author.id).get('0.0.0.5.6').format(Webpage_url = webpage_url), reference=False)
                    return None

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS, executable = "{0}/Bot/ffmpeg.exe".format(options.Path)), data=info)

    @staticmethod
    def parse_duration(duration: int, user_id: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        _duration = []
        if days > 0:
            _duration.append('{0} {1}'.format(days, Get_User_Lang(user_id).get('0.0.0.5.7')))
        if hours > 0:
            _duration.append('{0} {1}'.format(hours, Get_User_Lang(user_id).get('0.0.0.5.8')))
        if minutes > 0:
            _duration.append('{0} {1}'.format(minutes, Get_User_Lang(user_id).get('0.0.0.5.9')))
        if seconds > 0:
            _duration.append('{0} {1}'.format(seconds, Get_User_Lang(user_id).get('0.0.0.6.0')))

        return ', '.join(_duration)
