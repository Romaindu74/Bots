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
    def __init__(self, user_uuid: str, password: str) -> None:
        if not hasattr(importer, "Storage") or importer.Storage is None:
            raise ValueError("Storage is not available.")

        self.__user_permission_path = f"users-data/{user_uuid}.slze"

        self.__user_uuid = user_uuid

        self.__Storage: TypingStorage = importer.Storage("var/slazhe-users", __file__, SaveStorage, OpenStorage)
        self.__user_permission_ids: list[int] = self.__Storage.open(self.__user_permission_path, {}, password).get("permission", [])


# Version Globale: v00.00.00.0d
# Version du fichier: v00.00.00.04
