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
NOTSET    = 0

_levelToName = {
    CRITICAL: 'CRITICAL',
    ERROR:    'ERROR',
    WARNING:  'WARNING',
    INFO:     'INFO',
    DEBUG:    'DEBUG',
    NOTSET:   'NOTSET',
}

_nameToLevel = {
    'CRITICAL': CRITICAL,
    'ERROR':    ERROR,
    'WARNING':  WARNING,
    'INFO':     INFO,
    'DEBUG':    DEBUG,
    'NOTSET':   NOTSET,
}

_nameToColor = {
    'CRITICAL': colorama.Fore.RED,
    'ERROR':    colorama.Fore.RED,
    'WARNING':  colorama.Fore.YELLOW,
    'INFO':     colorama.Fore.GREEN,
    'DEBUG':    colorama.Fore.WHITE,
    'NOTSET':   colorama.Fore.WHITE

}

def getLevelName(level: Union[str, int]) -> Union[str, int]:
    result = _levelToName.get(level)
    if result is not None:
        return result
    result = _nameToLevel.get(level)
    if result is not None:
        return result
    return "Level %s" % level

def formatlevelName(level: str, max: int = 10) -> str:
    return (_nameToColor.get(level, colorama.Fore.WHITE)+(level+((max-len(level))*' ')))+colorama.Fore.WHITE

def Log(level: int = 0, text: str = '', _exit: bool = False, **options):
    context = '[{0}] [{1}] {2}'.format(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), formatlevelName(getLevelName(level), 8), str(text))

    if options.get('Log', True):
        print(context)

    try:
        with open('Logs.txt', 'a') as f:
            f.write(str(context)+'\n')
            f.close()

    except FileNotFoundError:
        with open('Logs.txt', 'w+') as f:
            f.write(str(context)+'\n')
            f.close()

    except Exception as e:
        raise Exception(str(e))

    if _exit:
        sys.exit(0)
