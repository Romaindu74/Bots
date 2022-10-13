import datetime
import colorama
import sys

from typing import Union

colorama.init(True)

CRITICAL  = 50
ERROR     = 40
WARNING   = 30
INFO      = 20
DEBUG     = 10
NOSET    = 0

_levelToName = {
    CRITICAL: 'CRITICAL',
    ERROR:    'ERROR',
    WARNING:  'WARNING',
    INFO:     'INFO',
    DEBUG:    'DEBUG',
    NOSET:    'NOSET',
}

_nameToLevel = {
    'CRITICAL': CRITICAL,
    'ERROR':    ERROR,
    'WARNING':  WARNING,
    'INFO':     INFO,
    'DEBUG':    DEBUG,
    'NOSET':    NOSET,
}

_nameToColor = {
    'CRITICAL': colorama.Fore.RED,
    'ERROR':    colorama.Fore.RED,
    'WARNING':  colorama.Fore.YELLOW,
    'INFO':     colorama.Fore.GREEN,
    'DEBUG':    colorama.Fore.WHITE,
    'NOSET':    colorama.Fore.WHITE
}

class Logger:
    def __init__(self) -> None:
        self.time_format = '%Y-%m-%d %H:%M:%S'

    def getLevel(self, level: Union[str, int]) -> str:
        if isinstance(level, str):
            return level
        
        return _levelToName.get(level, 'NOSET')

    def color(self, level: str) -> str:
        return _nameToColor.get(level, colorama.Fore.WHITE)

    def time(self) -> str:
        return datetime.datetime.now().strftime(self.time_format)

    def status(self, level: Union[int, str], max: int = 10) -> str:
        level = self.getLevel(level)
        color = self.color(level)

        return color + level + ((max - len(level)) * ' ') + colorama.Fore.WHITE

    def _save(self, text: str, level: int, max: int = 10) -> None:
        try:
            file = open('Logs.txt', 'a')
        except FileNotFoundError:
            file = open('Logs.txt', 'w+')
        except Exception as e:
            raise Exception(e)

        level = self.getLevel(level)

        file.write('[{0}] [{1}] {2}\n'.format(
                self.time(),
                level + (max - len(level)) * ' ',
                str(text)
            ))
        file.close()

    def _print(self, text: str, level: int, *args, **kwargs) -> None:
        context = '[{0}] [{1}] {2}'.format(
                self.time(),
                self.status(level),
                str(text)
            )

        if kwargs.get('Log', True):
            print(context)

        if kwargs.get('Save', True):
            self._save(text, level)

        if kwargs.get('Exit', False):
            sys.exit(0)

    def Critical(self, text: str, *args, **kwargs) -> None:
        self._print(text, CRITICAL, *args, **kwargs)

    def Error(self, text: str, *args, **kwargs) -> None:
        self._print(text, ERROR, *args, **kwargs)

    def Warn(self, text: str, *args, **kwargs) -> None:
        self._print(text, WARNING, *args, **kwargs)

    def Info(self, text: str, *args, **kwargs) -> None:
        self._print(text, INFO, *args, **kwargs)

    def Debug(self, text: str, *args, **kwargs) -> None:
        self._print(text, DEBUG, *args, **kwargs)

    def NoSet(self, text: str, *args, **kwargs) -> None:
        self._print(text, NOSET, *args, **kwargs)


def Log(level: int = 0, text: str = '', _exit: bool = False, **options):
    Logger()._print(text, level, Exit = _exit, **options)