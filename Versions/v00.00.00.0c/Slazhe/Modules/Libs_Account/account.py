from Slazhe import Logger

Log = Logger(__name__)

from Slazhe.Modules import importer

if getattr(importer, 'Storages', None):
    from Slazhe.Modules.Storage import Storage as TypingStorage

import json

from typing import Callable, Any

def OpenStorage(data: str) -> dict:
    try:
        return json.loads(data)
    except Exception as e:
        print(e)
        return {}

def SaveStorage(data: dict) -> str:
    return json.dumps(data)

class Account:
    def __init__(self, user_uuid: str) -> None:
        self.uuid = user_uuid

# Version Globale: v00.00.00.0c
# Version du fichier: v00.00.00.03
