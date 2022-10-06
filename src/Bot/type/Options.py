try:
    from requests import Session, Response
except Exception:
    raise

from typing import Union

from .Utils import MISSING

class Options:
    sessions:        Session
    Path:            str
    Initialized:     bool
    Info:            dict
    Bots:            dict

    def __init__(self)                                          -> None:...
    def Send(self, url: str = MISSING, *, stream: bool = False) -> Union[Response, None]:...
    def Start_Bots(self)                                        -> bool:...
    def add(self, Id: str = MISSING)                            -> bool:...
    def __bool__(self)                                          -> bool:...
    def __len__(self)                                           -> int:...

