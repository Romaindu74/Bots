from .Options import Options as _Options

import threading
import tkinter as tk

Types: list[str]
Status_: list[str]

class Status:
    Activity:  str
    Text:      str
    Statu:     str
    Time:      int
    Is_Config: bool

    def __init__(self, Bot: None, Options: _Options)                                         -> None:...
    def Interface(self, Activite: tk.Label, Statu: tk.Label, Time: tk.Label, Ping: tk.Label) -> None:...
    def Start(self)                                                                          -> None:...
    def Stop(self)                                                                           -> None:...
    def UpDate_Ping(self, ms: float)                                                         -> None:...

class Start(threading.Thread):
    def __init__(self, Bot: None, Options: _Options, main: Status) -> None:...
    def run(self)                                                  -> None:...
    def stop(self)                                                 -> None:...
    async def run_(self)                                           -> None:...
