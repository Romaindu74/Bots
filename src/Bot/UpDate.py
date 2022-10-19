from .GetLang                   import Code
from .Logger                    import Logger
from .Utils                     import decimal

_log = Logger(__name__)

import json
import pip
import os

from typing                     import Union
from time                       import monotonic
from typing                     import Union
from zipfile                    import ZipFile
from pip._internal.exceptions   import *

try:
    from requests               import Session, exceptions, Response
except ImportError:
    from pip._vendor.requests   import Session, exceptions, Response

class UpDate:
    URL     = 'https://raw.githubusercontent.com/Romaindu74/Bots/main/{Name}.{ext}'
    Session = Session()
    Path    = str(os.path.abspath('.'))

    def Start(self) -> bool:
        if not self.Modules():
            _log.Error(Code('0.0.2.5.1'))
            return False

        _log.Info(Code('0.0.2.5.2'))
        if not self.File():
            _log.Error(Code('0.0.2.5.3'))
            return False
        _log.Info(Code('0.0.2.5.4'))

        return True

    def send(self, url: str, ext: str = 'json', stream: bool = False) -> Union[Response, None]:
        try:
            request = self.Session.get(self.URL.format(Name = url, ext = ext), stream=stream)
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

    def Modules(self) -> bool:
        _log.Info(Code('0.0.2.5.5'))
        request = self.send('Modules')
        if request is None:
            return False

        try:
            modules = request.json()
        except exceptions.JSONDecodeError:
            return False
        else:
            _log.Info(Code('0.0.2.5.6'))
            for module in modules:
                try:
                    __import__(module)
                except (ImportError, ModuleNotFoundError):
                    try:
                        pip.main(['install', module])
                    except DistributionNotFound:
                        _log.Warn(Code('0.0.2.5.7').format(module = module))
                    except BestVersionAlreadyInstalled:
                        pass
            _log.Info(Code('0.0.2.5.8'))
            return True

    def File(self) -> bool:
        _log.Info(Code('0.0.2.5.9'))
        request = self.send('Version')

        if request is None:
            return False

        try:
            version       = request.json()
        except exceptions.JSONDecodeError:
            return False
        else:
            version: str  = version.get('Version', '0.0.0.0')[-1]

        _log.Info(Code('0.0.2.6.0').format(version = version))

        try:
            with open('{0}/User/__Json__/Main.json'.format(self.Path), 'r') as f:
                self.main: dict[str, str] = json.load(f)
                f.close()
        except FileNotFoundError:
            self.main = {'Version': '0.0.0.0'}

        bot_version = self.main.get('Version', '0.0.0.0')

        if version == bot_version:
            _log.Info(Code('0.0.2.6.1'))
            return True

        _log.Info(Code('0.0.2.6.2'))
        request = self.send(f'V {version}', 'zip', True)
        f = open(f'V {version}.file', 'wb')

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

        _log.Info(Code('0.0.2.6.3').format(seconde = round(monotonic() - time, 2)))
        _log.Info(Code('0.0.2.6.4'))

        with ZipFile(f'V {version}.file', 'r') as obj_zip:
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

        os.remove(f'V {version}.file')
        _log.Info(Code('0.0.2.6.5'))

        self.main['Version'] = version

        os.makedirs('{0}/User/__Json__/'.format(self.Path), 777, True)
        try:
            with open('{0}/User/__Json__/Main.json'.format(self.Path), 'w') as f:
                json.dump(self.main, f, indent = 4)
                f.close()
        except FileNotFoundError:
            with open('{0}/User/__Json__/Main.json'.format(self.Path), 'w+') as f:
                json.dump(self.main, f, indent = 4)
                f.close()

        return True
