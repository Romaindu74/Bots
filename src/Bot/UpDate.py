from typing import Union

from time     import monotonic
from typing   import Union
from zipfile  import ZipFile
from .Logger  import Log
from .Utils   import decimal
from pip._internal.exceptions import *

try:
    from requests             import Session, exceptions, Response
except ImportError:
    from pip._vendor.requests import Session, exceptions, Response

import json
import pip
import os

class UpDate:
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
            modules = request.json()
        except exceptions.JSONDecodeError:
            return False
        else:
            Log(20, 'Instalation des modules')
            for module in modules:
                try:
                    __import__(module)
                except (ImportError, ModuleNotFoundError):
                    try:
                        pip.main(['install', module])
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
            with open('{0}/User/__Json__/Main.json'.format(self.Path), 'r') as f:
                json.dump(self.main, f, ident = 4)
                f.close()
        except FileNotFoundError:
            bot_version = '0.0.0.0'

        return True
