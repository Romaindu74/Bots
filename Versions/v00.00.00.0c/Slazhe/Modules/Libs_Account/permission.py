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

class PermissionManager:
    def __init__(self, user_uuid: str, password: str):
        Log.Info(f"Utilisateur {user_uuid} a ouvert ses permissions.")

        if not hasattr(importer, "Storage") or importer.Storage is None:
            raise ValueError("Storage is not available.")

        self.__user_permission_path = f"users-permission/{user_uuid}.slze"

        self.__user_uuid = user_uuid

        self.__Storage: TypingStorage = importer.Storage("var/slazhe-users", __file__, SaveStorage, OpenStorage)
        self.__permissions_info: dict[int, dict[str, str]] = self.__Storage.open("custom-permission.slze", {})

        self.__user_permission_ids: list[int] = self.__Storage.open(self.__user_permission_path, {}, password).get("permission", [])

    def save(self, password: str) -> None:
        self.__Storage.save({"permission": self.__user_permission_ids}, self.__user_permission_path, password)

    def has_permission(self, permission_id: str) -> bool:
        return permission_id in self.__user_permission_ids

    def add_permission(self, permission_id: str) -> None:
        if not self.has_permission("permission:add"):
            raise PermissionError("Droits insuffisants pour ajouter une permission.")
        
        Log.Info(f"Permission {permission_id} ajoutée à {self.__user_uuid}.")
        
        if permission_id not in self.__permissions_info:
            raise ValueError("Permission inconnue.")
        
        if permission_id not in self.__user_permission_ids:
            self.__user_permission_ids.append(permission_id)

    def remove_permission(self, permission_id: str) -> None:
        if not self.has_permission("permission:remove"):
            raise PermissionError("Droits insuffisants pour retirer une permission.")
        
        if permission_id in self.__user_permission_ids:
            Log.Info(f"Permission {permission_id} retirée de {self.__user_uuid}.")
            self.__user_permission_ids.remove(permission_id)


    def list_permissions(self) -> list[str]:
        return [
            f"{pid} - {self.__permissions_info[pid]['name']} : {self.__permissions_info[pid]['description']}"
            for pid in self.__user_permission_ids if pid in self.__permissions_info
        ]

    def create_custom_permission(self, permission_id: str, name: str, description: str) -> None:
        if not self.has_permission("permission:create"):
            raise PermissionError("Droits insuffisants pour créer une permission.")
        
        if permission_id in self.__permissions_info:
            raise ValueError(f"ID {permission_id} déjà utilisé.")

        Log.Info(f"Permission personnalisée {permission_id} créée : {name}.")
        self.__permissions_info[permission_id] = {"name": name, "description": description}
        self.__Storage.save(self.__permissions_info, "custom-permission.slze")

    def get_permission_name(self, permission_id: str) -> str:
        return self.__permissions_info.get(permission_id, {}).get("name", "Inconnu")

    def get_all_permissions(self) -> dict:
        return self.__permissions_info

from functools import wraps

def require_permission(*required_ids: str, callback_pm: Callable[[PermissionManager], Any]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                pm: PermissionManager = callback_pm(*args, **kwargs)
            except Exception as e:
                raise PermissionError(f"Permission non accorder pour {func.__name__}")

            for permission_id in required_ids:
                if not pm.has_permission(permission_id):
                    Log.Warn(f"Accès refusé : {permission_id} requis pour {func.__name__}")
                    raise PermissionError(f"Permission requise : {permission_id}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
# Version Globale: v00.00.00.0c
# Version du fichier: v00.00.00.02
