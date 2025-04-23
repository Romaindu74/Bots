from .save import StorageSave
from .open import StorageOpen

from typing import Callable, Optional, Any, Union

class Storage(StorageSave, StorageOpen):
    def __init__(self, path: str, KeyOrUser: Union[list[int], Any], savefunc: Optional[Callable] = False, openfunc: Optional[Callable] = False, compression: Optional[bool] = False, encrypt: Optional[bool] = False) -> None:
        self.path: str  = path
        self.compression: bool  = compression
        self.encrypt: bool      = encrypt


        if savefunc:
            self.SaveFunctionFormat: Callable[[Any], str] = savefunc
    
        if openfunc:
            self.OpenFunctionFormat: Callable[[str], Any] = openfunc

        from Slazhe.SlazheModules import importer as SlazheImporter

        if getattr(SlazheImporter, "SlazheCrypto", False):
            self.slazhe_crypto          = SlazheImporter.SlazheCrypto()
            self.slazhe_crypto_password = SlazheImporter.SlazheCrypto.GSP(str(KeyOrUser)) if not isinstance(KeyOrUser, list) else KeyOrUser
# Version Globale: v00.00.00.0q
# Version du fichier: v00.00.00.01
