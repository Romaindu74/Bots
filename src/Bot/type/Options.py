from typing     import Union

try:
    from requests             import Session, Response
except ImportError:
    from pip._vendor.requests import Session, Response

class Options:
    Path:        str
    Initialized: bool
    Info:        dict
    sessions:    Session
    Bots:        dict

    def __len__(self)                                           -> int:...
    def __init__(self)                                          -> None:...
    def Start_Bots(self)                                        -> bool:...
    def add(self, Id: str)                                      -> bool:...
    def __bool__(self)                                          -> bool:...
    def Send(self, url: str, *, stream: bool = False)           -> Union[Response, None]:...
