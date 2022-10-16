from .Options import Options as _Options

from typing import Union
from typing_extensions import Self

from discord.ext import commands
import discord

import asyncio
import youtube_dl

class YTDLError(Exception):...

class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS:   dict[str, Union[str, bool]]
    FFMPEG_OPTIONS: dict[str, str]
    ytdl: youtube_dl.YoutubeDL

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5)              -> None:...
    def parse_duration(duration: int, user_id: int)                                                                            -> str:...
    async def create_source(cls, ctx: commands.Context, search: str, options: _Options, *, loop: asyncio.BaseEventLoop = None) -> Self:...
