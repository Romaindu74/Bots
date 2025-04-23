from Slazhe import Logger

Log = Logger(__package__)

from typing     import Optional, Any
from .CustomTypes import EBase

import pickle
import os, zlib

class StorageSave:
    def save(self, data: EBase, file: Optional[str] = None, password: Optional[str] = None) -> bool:
        if isinstance(data, EBase) and getattr(data, 'SlazheStorageFile', None):
            file = getattr(data, 'SlazheStorageFile', None)()

        if file is None:
            Log.Warn(f"No file name specified for {data.__class__.__name__}")
            return False

        slazhe_crypto_enable = hasattr(self, 'slazhe_crypto')

        FormatedData: Any = getattr(self, 'SaveFunctionFormat', lambda data: data)(data)

        if not isinstance(FormatedData, bytes):
            FormatedData = pickle.dumps(FormatedData)

        if password and slazhe_crypto_enable and False:
            result = ""
            try:
                result = self.slazhe_crypto.secure_encrypt(FormatedData, self.slazhe_crypto.get_secure_password(password))
            except Exception as e:
                print(e)
                pass

            if result != "":
                FormatedData = result

        if getattr(self, 'compression', True):
            ZlibCompressor: zlib._Compress = zlib.compressobj()
            CompressedData: bytes = ZlibCompressor.compress(FormatedData) + ZlibCompressor.flush()

        else:
            CompressedData: bytes = FormatedData

        if slazhe_crypto_enable and getattr(self, "encrypt", True):
            CompressedData: bytes = self.slazhe_crypto.secure_encrypt(CompressedData, self.slazhe_crypto_password)

        File: str = os.path.abspath(f'{self.path}/{file}')
        Path: str = os.path.dirname(File)

        os.makedirs(Path, 611, exist_ok = True)

        try:
            IOFile = open(File, 'wb+')
        except Exception as e:
            return False

        else:
            try:
                IOFile.write(CompressedData)
                IOFile.flush()
            except Exception as e:
                return False
            finally:
                IOFile.close()
            return True

# Version Globale: v00.00.00.0s
# Version du fichier: v00.00.00.01
