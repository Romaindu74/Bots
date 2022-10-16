from typing import Union

try:
    from requests             import Session, Response
except ImportError:
    from pip._vendor.requests import Session, Response

class UpDate:
    URL:     str
    Path:    str
    Session: Session

    def Start(self)                                                   -> bool:...
    def Modules(self)                                                 -> bool:...
    def File(self)                                                    -> bool:...
    def send(self, url: str, ext: str = 'json', stream: bool = False) -> Union[Response, None]:...