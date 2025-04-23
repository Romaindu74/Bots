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

class LoginManager:
    def __init__(self) -> None:
        if not hasattr(importer, "Storage") or importer.Storage is None:
            raise ValueError("Storage is not available.")

        self.__Storage: TypingStorage = importer.Storage("var/slazhe-users", __file__, SaveStorage, OpenStorage)


import hashlib
import secrets
from datetime import datetime, timedelta




class Session:
    def __init__(self, account: Account, duration_minutes: int = 30):
        self.account = account
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(minutes=duration_minutes)
        self.token = secrets.token_hex(32)  # 64 caractères, très solide

    def is_active(self) -> bool:
        return datetime.now() < self.expires_at

class LoginManager:
    def __init__(self, user_db: dict):
        self.user_db = user_db
        self.__sessions_by_token: dict[str, Session] = {}  # attribut privé

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username: str, password: str) -> str:
        user = self.user_db.get(username)
        if not user:
            raise ValueError("Utilisateur introuvable")

        if self.hash_password(password) != user["password_hash"]:
            raise ValueError("Mot de passe incorrect")

        account = Account(user["id"], user["username"], user["permissions"])
        session = Session(account)
        self.__sessions_by_token[session.token] = session

        return session.token  # renvoie le token unique

    def get_account_from_token(self, token: str) -> Account | None:
        session = self.__sessions_by_token.get(token)
        if session and session.is_active():
            return session.account
        return None

    def logout(self, token: str):
        if token in self.__sessions_by_token:
            del self.__sessions_by_token[token]
# Version Globale: v00.00.00.0p
# Version du fichier: v00.00.00.06
