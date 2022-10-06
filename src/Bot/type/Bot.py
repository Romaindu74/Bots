from .Interface import Interface as I
from .Options   import Options   as O
from .Statu     import Statu_    as S
from .Utils     import MISSING

try:
    import discord
    from discord.ext import commands
except Exception:
    raise

class Bot:
    _initialized:  bool
    _error      :  bool
    Initialized:   bool
    Error:         bool
    Status_:        str
    Id:            str
    Interface:     I    
    Options:       O
    Status:        S
    Ping:          float
    Client:        commands.Bot
    Prefix:        dict
    Info:          dict
    def __init__(self, Id: str = MISSING, Options: O = MISSING)        -> None:...
    async def _Start(self)                                             -> None:...
    def _prefix_(self, client: commands.Bot, message: discord.Message) -> list:...
    def Stop(self)                                                     -> bool:...
    def Start(self)                                                    -> bool:...