import os
from typing     import Self, Union, Optional, Literal, Dict
from io         import TextIOWrapper
from datetime   import datetime as dt
import shutil

try:
    import colorama
except ImportError:
    class colorama:
        class Color:
            RED     = ''
            YELLOW  = ''
            GREEN   = ''
            WHITE   = ''

        def init(self) -> None:pass
        Fore = Color()

colorama.init(True)

class Levels:
    CRITICAL:   Literal['50'] = 50
    ERROR:      Literal['40'] = 40
    WARNING:    Literal['30'] = 30
    INFO:       Literal['20'] = 20
    DEBUG:      Literal['10'] = 10
    NOSET:      Literal['0']  = 0

    LevelToName: dict[int, str] = {
        CRITICAL: 'CRITICAL',
        ERROR:    'ERROR',
        WARNING:  'WARNING',
        INFO:     'INFO',
        DEBUG:    'DEBUG',
        NOSET:    'NOSET',
    }

    NameToLevel: dict[str, int] = {
        'CRITICAL': CRITICAL,
        'ERROR':    ERROR,
        'WARNING':  WARNING,
        'INFO':     INFO,
        'DEBUG':    DEBUG,
        'NOSET':    NOSET,
    }

    NameToColor: dict[str, str] = {
        'CRITICAL': colorama.Fore.RED,
        'ERROR':    colorama.Fore.RED,
        'WARNING':  colorama.Fore.YELLOW,
        'INFO':     colorama.Fore.GREEN,
        'DEBUG':    colorama.Fore.WHITE,
        'NOSET':    colorama.Fore.WHITE
    }

    ColorToColor: dict[str, str] = {
        'RED'   : colorama.Fore.RED,
        'YELLOW': colorama.Fore.YELLOW,
        'GREEN' : colorama.Fore.GREEN,
        'WHITE' : colorama.Fore.WHITE
    }

class LoggerConfig:
    _config: dict[str, str] = {}
    _initialized: bool = False

    @classmethod
    def init(cls, TimeFormat: Optional[str] = '%Y-%m-%d %H:%M:%S', FileFormat: Optional[str] = '%Y-%m-%d', Folder: Optional[str] = '/', Level: int = Levels.NOSET) -> None:
        if not cls._initialized:
            cls._config = {
                'TF': TimeFormat,
                'FF': FileFormat,
                'FileFolder': Folder,
                'Level': Level
            }
            cls._initialized = True

    @classmethod
    def get_config(cls) -> dict[str, str]:
        return cls._config

    @classmethod
    def update_config(cls, new_config: dict[str, str]) -> None:
        cls._config.update(new_config)

class LogProgressBar:
    def __init__(self, total: int) -> None:
        self.total: int = total
        self.last: int = 0
        self._index: Dict[int, str] = {}

    def add(self, index: int, color: Optional[str] = 'white') -> None:
        self._update_index(color)
        self.last += index
        self._check_bounds()
        self.print()

    def remove(self, index: int, color: Optional[str] = 'white') -> None:
        self._update_index(color)
        self.last -= index
        self._check_bounds()
        self.print()

    def index(self, index: int, color: Optional[str] = 'white') -> None:
        self._update_index(color)
        self.last = index
        self._check_bounds()
        self.print()

    def _update_index(self, color: str) -> None:
        position = int((self.last / self.total) * (shutil.get_terminal_size().columns - 10))
        self._index[position] = getattr(colorama.Fore, color.upper(), colorama.Fore.WHITE)

    def _check_bounds(self) -> None:
        if self.last < 0:
            self.last = 0
        elif self.last > self.total:
            self.last = self.total

    def print(self) -> None:
        terminal_width = shutil.get_terminal_size().columns
        percent = (self.last / self.total) * 100
        num_equals = int((self.last / self.total) * (terminal_width - 10))
        num_dashes = terminal_width - 10 - num_equals

        bar = ''
        for num_eq in range(num_equals):
            if num_eq in self._index:
                bar += self._index[num_eq]
            bar += '='
        bar += colorama.Fore.WHITE + '-' * num_dashes
        print(f"\r[{bar}] {percent:.2f}%", end="")

class Logger:
    _instances: dict[str, Self] = {}
    Logs: list[str]

    _Levels: Levels
    _Name: str

    _Running: dict[str, Union[TextIOWrapper]]

    _default_color: str = colorama.Fore.WHITE

    def __new__(cls, Name: Optional[str] = None) -> Self:
        if Name in cls._instances:
            return cls._instances[Name]

        instance = super().__new__(cls)
        cls._instances[Name] = instance

        instance._Levels    = Levels()
        instance._Running   = {}
        instance.Logs       = []
        instance._Name      = Name.split('.')[-1] if Name else ''

        return instance

    def __init__(self, Name: Optional[str] = None):
        self._Name = Name.split('.')[-1] if Name else ''

    @property
    def _Config(self) -> dict[str, str]:
        return LoggerConfig.get_config()
    
    @property
    def initialised(self) -> bool:
        return LoggerConfig._initialized

    def __gL(self, L: Union[str, int]) -> str:
        return L if isinstance(L, str) else self._Levels.LevelToName.get(L, 'NOSET')

    def __gC(self, L: str) -> str:
        return self._Levels.NameToColor.get(L, self._default_color)

    def __gT(self, format: str) -> str:
        return dt.now().strftime(format)

    def __getStatus(self, Level: Union[str, int], Color: Optional[bool] = True, Size: Optional[int] = 10) -> str:
        L: str = self.__gL(Level)

        return f"{self.__gC(L)}{L}{' ' * (Size - len(L))}{self._default_color}" if Color else f"{L}{' ' * (Size - len(L))}"

    def __getName(self, Size: Optional[int] = 20) -> str:
        return f"{self._Name}{(Size - len(self._Name)) * ' '}"

    def __getCommentFormat(self, Level: Union[str, int], Comment: str, Color: Optional[bool] = True) -> str:
        return '[{0}] [{1}] [{2}] {3}'.format(
            self.__gT(self._Config.get('TF')),
            self.__getName(),
            self.__getStatus(Level, Color),
            str(Comment)
        )

    def Save(self, Level: Union[str, int], Comment: str) -> None:
        os.makedirs(self._Config.get('FileFolder', '/'), exist_ok = True)

        FileName = self.__gT(self._Config.get('FF'))
        if not self._Running.get('File', False) or FileName != self._Running.get('FF', ''):
            if FileName != self._Running.get('FF', '') and self._Running.get('File', False):
                self._Running['File'].flush()
                self._Running['File'].close()

            try:
                File = open(f"{self._Config.get('FileFolder', '/')}{FileName}", 'a')
            except FileNotFoundError:
                File = open(f"{self._Config.get('FileFolder', '/')}{FileName}", 'w+')
            except Exception:
                File = None
            finally:
                self._Running['File'] = File
                self._Running['FF'] = FileName

        self._Running['File'].write(self.__getCommentFormat(Level, Comment, False) + '\n')

    def Print(self, *Comments: str, Level: Union[str, int], Save: Optional[bool] = False, JoinFormat: Optional[str] = ' ', Print: Optional[bool] = True) -> None:
        if not self.initialised:
            raise Exception('Logger is not initialised.')

        Comment = JoinFormat.join([str(Comment) for Comment in Comments])

        self.Logs.append(
            self.__getCommentFormat(Level, Comment, False)
        )

        if Save:
            self.Save(Level, Comment)

        if Print and self._Config.get('Level', 0) <= Level:
            print(
                self.__getCommentFormat(Level, Comment, True)
            )

    def Critical(self, *text: str, **kwargs) -> None:
        self.Print(*text, Level = Levels.CRITICAL, Save = True, **kwargs)

    def Error(self, *text: str, **kwargs) -> None:
        self.Print(*text, Level = Levels.ERROR, Save = True, **kwargs)

    def Warn(self, *text: str, **kwargs) -> None:
        self.Print(*text, Level = Levels.WARNING, Save = True, **kwargs)

    Warning = Warn

    def Info(self, *text: str, **kwargs) -> None:
        self.Print(*text, Level = Levels.INFO, Save = True, **kwargs)

    def Debug(self, *text: str, **kwargs) -> None:
        self.Print(*text, Level = Levels.DEBUG, **kwargs)

    def NoSet(self, *text: str, **kwargs) -> None:
        self.Print(*text, Level = Levels.NOSET, **kwargs)

    def reload(self) -> None:
        import importlib, sys

        if 'colorama' in sys.modules:
            return
        else:
            import colorama
            importlib.reload(colorama)

        colorama.init(True)

        self._Levels.NameToColor = {
            'CRITICAL': colorama.Fore.RED,
            'ERROR':    colorama.Fore.RED,
            'WARNING':  colorama.Fore.YELLOW,
            'INFO':     colorama.Fore.GREEN,
            'DEBUG':    colorama.Fore.WHITE,
            'NOSET':    colorama.Fore.WHITE
        }
        self._default_color = colorama.Fore.WHITE

# Version Globale: v00.00.00.0k
# Version du fichier: v00.00.00.01
