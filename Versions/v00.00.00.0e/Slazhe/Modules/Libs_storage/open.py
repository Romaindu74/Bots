from Slazhe import Logger

Log = Logger(__package__)

from typing         import Optional, Any, Callable
from .CustomTypes   import EBase, to_extended

import pickle
import os, zlib

class StorageOpen:
    def GDB(self, value: Any) -> Callable:
        def decorator() -> Any:
            return value
        return decorator

    def open(self, file: str, default: Optional[Any] = None, password: Optional[str] = None) -> EBase:
        File: str = os.path.abspath(f'{self.path}/{file}')
        Path: str = os.path.dirname(File)

        os.makedirs(Path, exist_ok = True)

        try:
            IOFile = open(File, 'rb')
        except FileNotFoundError:
            result = to_extended(default)
            result.SlazheStorageFile = self.GDB(file)
            return result

        except Exception as e:
            result = to_extended(default)
            result.SlazheStorageFile = self.GDB(file)
            return result

        CompressedData: bytes = IOFile.read()
        IOFile.close()

        slazhe_crypto_enable = hasattr(self, 'slazhe_crypto')
        if slazhe_crypto_enable:
            try:
                DecryptedData: bytes = self.slazhe_crypto.secure_decrypt(CompressedData, self.slazhe_crypto_password)
            except Exception:
                DecryptedData: bytes = CompressedData

            if DecryptedData == "":
                DecryptedData: bytes = CompressedData

        else:
            DecryptedData: bytes = CompressedData

        ZlibDecompressor: zlib._Decompress = zlib.decompressobj()
        try:
            DecompressedData: bytes = ZlibDecompressor.decompress(DecryptedData)
        except Exception:
            DecompressedData: bytes = DecryptedData

        if password and slazhe_crypto_enable:
            result = ""
            try:
                result = self.slazhe_crypto.secure_decrypt(DecompressedData, self.slazhe_crypto.get_secure_password(password))
            except Exception:
                pass

            if result != "":
                DecompressedData = result

        try:
            Data = pickle.loads(DecompressedData, encoding="utf-8", errors="replace")
        except pickle.UnpicklingError:
            Data = DecompressedData.decode("utf-8", "replace")

        FormatedData: Any = getattr(self, 'OpenFunctionFormat', lambda data: data)(Data)

        result = to_extended(FormatedData)
        result.SlazheStorageFile = self.GDB(file)


        return result

# Version Globale: v00.00.00.0e
# Version du fichier: v00.00.00.01
