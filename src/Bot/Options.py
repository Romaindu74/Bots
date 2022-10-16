from .Utils     import Save, Open, MISSING
from .GetLang   import Get_Lang
from .Bot       import Bot as _Bots
from .Logger    import Logger

from typing     import Union

import os

_log = Logger(__name__)

try:
    from requests             import Session, exceptions, Response
except ImportError:
    from pip._vendor.requests import Session, exceptions, Response
    _log.Critical(Get_Lang.get('0.0.0.0.0').format(Name = 'requests'))
except Exception as e:
    _log.Critical(Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)


class Options:
    def __init__(self) -> None:
        self._info: dict          = {
            'Windows-Title': 'RPA-Bot\'s'
        }

        self._path: str           = os.path.abspath('.')
        self._bots: dict[_Bots]   = {}

        self._initialized: bool   = self.Start_Bots()

        self._sessions            = Session()

    def Send(self, url: str = MISSING, *, stream: bool = False) -> Union[Response, None]:
        if url is MISSING:
            return None

        try:
            request = self._sessions.get(url, stream=stream)
        except exceptions.HTTPError as error:
            _log.Critical(f"Request: {url}\nHttp Error: {error}")
        except exceptions.ConnectionError as error:
            _log.Critical(f"Request: {url}\nError Connecting: {error}")
        except exceptions.Timeout as error:
            _log.Critical(f"Request: {url}\nTimeout Error: {error}")
        except exceptions.RequestException as error:
            _log.Critical(f"Request: {url}\nError: {error}")
        else:
            return request

        return None


    def Start_Bots(self) -> bool:
        try:
            _log.Info(Get_Lang.get('0.0.1.7.0'))
            if not os.path.exists('{0}/User/Bots/Bots.json'.format(self.Path)):
                os.makedirs('{0}/User/Bots'.format(self.Path), exist_ok = True)
                Save('{0}/User/Bots/Bots.json'.format(self.Path), {'Bots': []})
        except Exception as e:
            _log.Critical(Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)))
            return False

        _log.Info('Chargement des bot')
        for Bot in Open('{0}/User/Bots/Bots.json'.format(self.Path), {'Bots': []}).get('Bots', []):
            Bot_ = _Bots(Bot, self)

            if Bot_.Initialized and not Bot_.Error:
                Bot_.start()
                self._bots[Bot] = Bot_

        _log.Info('Les bot ont corectement été charger')
        return True

    def add(self, Id: str = MISSING) -> bool:
        if not Id == MISSING:
            Bot_ = _Bots(Id, self)

            while not Bot_.Initialized and not Bot_.Error:
                pass

            _log.Info('Lancement du bot')
            Bot_.start()
            self._bots[Id] = Bot_

            return True
        else:
            _log.Warn('L\'id du bot est manquant')
            return False

    def __bool__(self) -> bool:
        return self._initialized

    def __len__(self) -> int:
        return len(self._bots)

    @property
    def sessions(self) -> Session:
        return self._sessions

    @property
    def Path(self) -> str:
        return self._path

    @property
    def Initialized(self) -> bool:
        return self._initialized

    @property
    def Info(self) -> dict:
        return self._info

    @Info.setter
    def Info(self, value: dict = MISSING) -> dict:
        if not value == MISSING:
            self._info = value
        return self._info

    @property
    def Bots(self) -> dict[_Bots]:
        return self._bots

    @Bots.setter
    def Bots(self, value: dict[_Bots] = MISSING) -> dict[_Bots]:
        if not value == MISSING:
            self._bots = value
        return self._bots