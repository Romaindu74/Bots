from .Options   import Options   as _Options
from .Status    import Status    as _Status
from .Interface import Interface as _Interface

from discord.ext import commands

import threading
import discord


class Bot(threading.Thread):
    Ping:         float
    _initialized: bool
    _error:       bool
    Initialized:  bool
    Error:        bool
    Prefix:       dict
    Info:         dict
    Id:           str
    Status_:      str
    Status:       _Status
    Options:      _Options
    Interface:    _Interface
    Client:       commands.Bot

    def __init__(self, Id: str, Options: _Options)                     -> None:...
    def run(self)                                                      -> None:...
    async def _Start(self)                                             -> None:...
    def Stop(self)                                                     -> bool:...
    def Start(self)                                                    -> bool:...
    def _prefix_(self, client: commands.Bot, message: discord.Message) -> list:...

