from Slazhe import Logger

Log = Logger(__name__)

from Slazhe.Modules import importer

if getattr(importer, 'Storages', None):
    from Slazhe.Modules.Storage import Storage as TypingStorage

import json

from typing         import Any
from .permission    import PermissionManager

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

        self.__user_storage_path = f"users-data/{user_uuid}.slze"

        self.__user_uuid = user_uuid

        self.__Storage: TypingStorage = importer.Storage("var/slazhe-users", __file__, SaveStorage, OpenStorage)
        self.__user_data: dict[Any] = self.__Storage.open(self.__user_storage_path, {}, password)

        self.__permission: PermissionManager = PermissionManager(user_uuid, password)

    @property
    def name(self) -> str:
        return self.__user_data.get("name", "Unknown")
    
    @property
    def uuid(self) -> str:
        return self.__user_uuid
    
    @property
    def force_reset_password(self) -> bool:
        return self.__user_data.get("reset_password", False)

    def has_permission(self, permission_id: str) -> bool:
        return self.__permission.has_permission(permission_id)
# Version Globale: v00.00.00.0s
# Version du fichier: v00.00.00.0f
