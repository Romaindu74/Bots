import sys

from typing import Union

from datetime import datetime
from time     import monotonic
from typing   import Union
from zipfile import ZipFile

_levelToName = {50: 'CRITICAL', 40: 'ERROR', 30: 'WARNING', 20: 'INFO', 10: 'DEBUG', 0: 'NOTSET'}

def Log(Level: _levelToName, text: str, exit: bool = False, **options) -> Union[str, None]:
    context = '[{0}] [{1}] : {2}'.format(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        _levelToName.get(Level, 0),
        text
    )

    if options.get('Print', True):
        print(context)

    try:
        with open(
            'Logs.txt',
            'a'
        ) as file:
            file.write(context+'\n')
            file.close()

    except FileNotFoundError:
        with open(
            'Logs.txt',
            'w+'
        ) as file:
            file.write(context+'\n')
            file.close()

    except Exception as e:
        raise Exception(str(e))

    if exit:
        sys.exit(0)

    return context

def _to_str(size: int, suffixes: tuple, base: int, *, precision: int = 1, separator: str = " ") -> str:
    if size == 1:
        return "1 byte"
    elif size < base:
        return "{:,} bytes".format(size)

    for i, suffix in enumerate(suffixes, 2):  # noqa: B007
        unit = base**i
        if size < unit:
            break
    return "{:,.{precision}f}{separator}{}".format(
        (base * size / unit),
        suffix,
        precision=precision,
        separator=separator,
    )

def decimal(size: int, *, precision: int = 1, separator: str = " ") -> str:
    return _to_str(
        size,
        ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"),
        1000,
        precision=precision,
        separator=separator,
    )

try:
    from requests             import Session, exceptions, Response
except ImportError:
    from pip._vendor.requests import Session, exceptions, Response

import json
import pip
import os
from pip._internal.exceptions import *

class Instalateur:
    URL     = 'https://raw.githubusercontent.com/Romaindu74/Bots/main/{Name}.{ext}'
    Session = Session()
    Path    = str(os.path.abspath('.'))

    def Start(self) -> bool:
        if not self.Modules():
            Log(40, 'Une erreur est survenue lors de la verification des modules')
            return False

        if not self.File():
            Log(40, 'Une erreur est survenue lors du telechargement des fichier')
            return False

        return True

    def send(self, url: str, ext: str = 'json', stream: bool = False) -> Union[Response, None]:
        try:
            request = self.Session.get(self.URL.format(Name = url, ext = ext), stream=stream)
        except exceptions.HTTPError as error:
            Log(50, f"Request: {url}\nHttp Error: {error}")
        except exceptions.ConnectionError as error:
            Log(50, f"Request: {url}\nError Connecting: {error}")
        except exceptions.Timeout as error:
            Log(50, f"Request: {url}\nTimeout Error: {error}")
        except exceptions.RequestException as error:
            Log(50, f"Request: {url}\nError: {error}")
        else:
            return request
        return None

    def Modules(self) -> bool:
        Log(20, 'Recuperation des modules requis')
        request = self.send('Modules')
        if request is None:
            return False

        try:
            modules: dict[str, str] = request.json()
        except exceptions.JSONDecodeError:
            return False
        else:
            Log(20, 'Instalation des modules')
            for module in modules:
                try:
                    __import__(module)
                except ImportError:
                    try:
                        pip.main(['install', modules[module]])
                    except DistributionNotFound:
                        Log(30, f'Module {module} is not found')
                    except BestVersionAlreadyInstalled:
                        pass
            Log(20, 'Instalation des modules fini')
            return True
        Log(50, 'Un erreur est survenu')
        return False

    def File(self) -> bool:
        Log(20, 'Recuperation de la derniere version')
        request = self.send('Version')

        if request is None:
            return False

        try:
            version       = request.json()
        except exceptions.JSONDecodeError:
            return False
        else:
            version: str  = version.get('Version', '0.0.0.0')[-1]

        Log(20, 'Version trouvé: {0}'.format(version))

        try:
            with open('{0}/User/__Json__/Main.json'.format(self.Path), 'r') as f:
                self.main = json.load(f)
                f.close()
        except FileNotFoundError:
            bot_version = '0.0.0.0'
        else:
            bot_version = self.main.get('Version', '0.0.0.0')

        if version == bot_version:
            Log(20, 'Les version coresponde')
            return True

        Log(20, 'Lancement de l\'instalation')
        request = self.send(f'V {version}', 'zip', True)
        f = open(f'V {version}.zip', 'wb')

        block = 1024 * 512
        size  = int(request.headers.get('content-length'))
        pack  = 0
        time  = monotonic()

        for chunk in request.iter_content(block):
            if chunk:
                try:
                    f.write(chunk)
                except Exception:
                    return False
                else:
                    pack += len(chunk)
                    if ((pack / size) * 100) > 100:
                        file_total = 100
                    else:
                        file_total = (pack / size) * 100

                    print('[{0}] {1} {2}'.format((int(file_total/2) * '-') + ((50 - int(file_total/2)) * ' '), str(round(file_total, 2)) + '%', decimal(len(chunk))), end = '\r')
        f.close()
        print('\n')

        Log(20, 'Telechargement fini en {0}s'.format(round(monotonic() - time, 2)))
        Log(20, 'Decompilation')

        with ZipFile(f'V {version}.zip', 'r') as obj_zip:
            Files = obj_zip.namelist()
            for File in Files:
                if File.find('.') < 0:
                    os.makedirs(File, 777, True)

                else:
                    file = open(File, 'wb')
                    with obj_zip.open(File, 'r') as f:
                        for line in f.readlines():
                            file.write(line)
                    file.close()

        os.remove(f'V {version}.zip')
        Log(20, 'l\'installation a été terminé avec succès')

        try:
            os.makedirs('{0}/User/__Json__/'.format(self.Path), 777, True)
            with open('{0}/User/__Json__/Main.json'.format(self.Path), 'w+') as f:
                json.dump({'Version': version, 'Lang': 'English'}, f, indent=4)
                f.close()
        except Exception as e:
            Log(50, str(e))
            return False

        return True

if __name__ == '__main__':
    Instalateur().Start()