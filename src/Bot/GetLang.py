import os
import json
from typing import Union

from .Logger import Log

try:
    from requests             import Session
except ImportError:
    from pip._vendor.requests import Session
    Log(50, 'Module requests is not found', True)
except Exception as e:
    Log(50, "An error occurred in file {0}\nError: {1}".format(__file__, e), True)

class Get_Lang:
    @classmethod
    def get(self, code: str = False, __default: str = False, **options) -> Union[str, bool, None]:
        if not code:
            return False

        path: str = os.path.abspath('.')
        session: Session = Session()

        if options.get('Lang', False):
            Lang: dict = {'Lang': options.get('Lang')}

        else:
            try:
                os.makedirs('{0}/User/__Json__/'.format(path), 777, True)
                with open('{0}/User/__Json__/Main.json'.format(path), 'r', encoding="utf-8") as f:
                    Lang: dict = json.load(f)
                    f.close()
            except FileNotFoundError:
                Lang = {'Lang': 'English'}
                os.makedirs('{0}/User/__Json__/'.format(path), 777, True)
                with open('{0}/User/__Json__/Main.json'.format(path), 'w+', encoding="utf-8") as f:
                    json.dump(Lang, f, indent=4)
                    f.close()
            except Exception as e:
                Log(50, 'Error in file GetLang.py\nError: {0}'.format(e))
                Lang = {'Lang': 'English'}

        try:
            with open('{0}/Bot/Language/{1}.json'.format(path, Lang.get('Lang', 'English')), 'r', encoding="utf-8") as f:
                self.file_lang: dict = json.load(f)
                f.close()
        except FileNotFoundError:
            Log(20, 'File {0}.json download'.format(Lang.get('Lang')))
            os.makedirs('{0}/Bot/Language/'.format(path), 777, True)
            f = open('{0}/Bot/Language/{1}'.format(path, str(Lang.get('Lang'))+'.json'), 'wb+')
            with session.get('https://raw.githubusercontent.com/Romaindu74/Bots/main/Language/{0}'.format(str(Lang.get('Lang'))+'.json')) as r:
                try:
                    f.write(r.content)
                except Exception as e:
                    Log(50, "An error occurred in file {0}\nError: {1}".format(__file__, e))
                    return False
                f.close()
            Log(20, 'Download completed')

            with open('{0}/Bot/Language/{1}.json'.format(path, Lang.get('Lang', 'English')), 'r', encoding="utf-8") as f:
                self.file_lang = json.load(f);f.close();del f
        except Exception as e:
            Log(50, 'Error in file GetLang.py\nError: {0}'.format(e), True)
            return False

        session.close()
        if __default:
            return self.file_lang.get(code, __default)
        return self.file_lang.get(code, self.get(code, 'None', Lang = 'English'))

class Get_User_Lang:
    def __init__(self, id: int, Lang: str = False):
        path = os.path.abspath('.')

        self.id = id

        if not Lang:
            os.makedirs('{0}/User/__User__/'.format(path), 777, True)
            try:
                with open('{0}/User/__User__/{1}.json'.format(path, id), 'r', encoding="utf-8") as f:
                    self.main_file = json.load(f);f.close();del f
            except FileNotFoundError:
                self.main_file = {"Lang": "English"}
                with open('{0}/User/__User__/{1}.json'.format(path, id), 'w+', encoding="utf-8") as f:
                    json.dump(self.main_file, f, indent=4);f.close();del f
            except Exception as e:
                self.main_file = {'Lang': 'English'}
                Log(50, 'Error in file GetLang.py\nError: {0}'.format(e))
        else:
            self.main_file = {"Lang": Lang}

    def get(self, __key: str, __default: str = False) -> str:
        return Get_Lang.get(__key, __default, Lang = self.main_file.get('Lang', 'English'))

    @property
    def get_lang(self) -> str:
        return self.main_file.get('Lang', 'English')