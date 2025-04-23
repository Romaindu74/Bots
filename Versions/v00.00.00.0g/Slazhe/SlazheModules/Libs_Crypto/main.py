from ctypes import CDLL, c_char_p, c_int, POINTER, byref, c_uint, c_ubyte
from typing import Self, Optional

import os

SCryptoTypes = {
    'GetSecureKey': {
        'return': None,
        'args': [c_char_p, POINTER(c_int), POINTER(c_int)]
    },
    'SecureEncrypt': {
        'return': c_int,
        'args': [POINTER(c_ubyte), c_uint, POINTER(c_int), c_uint, POINTER(c_ubyte), c_uint, c_uint, POINTER(c_ubyte), c_uint, POINTER(c_ubyte)]
    },
    'SecureDecrypt': {
        'return': c_int,
        'args': [POINTER(c_ubyte), c_uint, POINTER(c_int), c_uint, POINTER(c_ubyte), c_uint, c_uint, POINTER(c_ubyte), c_uint, POINTER(c_ubyte)]
    }
}

class SCryptoTyping:
    def GetSecureKey(self, A: c_char_p, B: c_int, C: c_int)                                                                                 -> None:pass
    def SecureEncrypt(self, A: c_ubyte, B: c_uint, C: c_int, D: c_uint, E: c_ubyte, F: c_uint, G: c_uint, H: c_ubyte, I: c_uint, J: c_ubyte) -> c_int:pass
    def SecureDecrypt(self, A: c_ubyte, B: c_uint, C: c_int, D: c_uint, E: c_ubyte, F: c_uint, G: c_uint, H: c_ubyte, I: c_uint, J: c_ubyte)-> c_int:pass

class Crypto:
    instance: Self          = None
    _is_initialized: bool    = False

    def __new__(cls, new_instance: Optional[bool] = False):
        if new_instance or cls.instance is None:
            self = super().__new__(cls)

            if cls.instance is None:
                cls.instance = self
        else:
            self = cls.instance

        return self
    
    def is_initialized(self) -> bool:
        if not self.instance:
            return False
        
        return self.instance._is_initialized

    def config(self, Path: str = None, **Options) -> None:
        self.SCrypto = CDLL(Path or os.path.join(os.path.dirname(__file__), "DLL", "SlazheCrypto.dll"))

        self.Params: dict[str, int] = {
            'SaltSize': Options.get('SaltSize', 16),
            'KeySize': Options.get('KeySize', 32),
            'IvSize': Options.get('IvSize', 16),
            'Iterations': Options.get('Iterations', 10000)
        }

        for Func in SCryptoTypes:
            try:
                Element = getattr(self.SCrypto, Func)
            except AttributeError:
                continue

            else:
                Element.restype     = SCryptoTypes[Func]['return']
                Element.argtypes    = SCryptoTypes[Func]['args']

        self._is_initialized = True

    def secure_decrypt(self, encrypted_data: bytes, password: list[int]) -> bytes:
        # return encrypted_data.decode("utf-8", errors="replace")
        salt_len = self.Params['SaltSize']
        iv_len = self.Params['IvSize']

        # Vérifier que la longueur du message est suffisante
        if len(encrypted_data) < (salt_len + iv_len):
            raise ValueError("Invalid encrypted data format.")

        # Extraire salt, iv et ciphertext à partir des bytes
        salt        = encrypted_data[:salt_len]
        iv          = encrypted_data[salt_len:salt_len + iv_len]
        ciphertext  = encrypted_data[salt_len + iv_len:]

        ciphertext_len  = len(ciphertext)
        salt_len        = len(salt)
        iv_len          = len(iv)

        if iv_len != self.Params['IvSize']:
            raise ValueError("IV size does not match expected size.")

        if salt_len != self.Params['SaltSize']:
            raise ValueError("Salt size does not match expected size.")

        ciphertext_array= (c_ubyte * ciphertext_len)(*ciphertext)
        salt_array      = (c_ubyte * salt_len)(*salt)
        iv_array        = (c_ubyte * iv_len)(*iv)

        plaintext       = (c_ubyte * (ciphertext_len * 4))()
        password_array  = (c_int * len(password))(*password)


        result = self.SCrypto.SecureDecrypt(
            ciphertext_array, ciphertext_len,
            password_array, len(password),
            salt_array, salt_len,
            self.Params['Iterations'],
            iv_array, iv_len,
            plaintext
        )

        if result < 0:
            raise RuntimeError(f"Decryption failed with error code: {result}")

        return bytes(plaintext[:result])
    
    def secure_encrypt(self, PlainTextData: bytes, password: list[int]) -> bytes:
        PlainText = PlainTextData

        # return PlainText

        PlainText_len   = len(PlainText)
        salt_len        = self.Params.get('SaltSize', 16)
        iv_len          = self.Params.get('IvSize', 16)

        plaintext_array = (c_ubyte * PlainText_len)(*PlainText)
        salt            = (c_ubyte * salt_len)()
        iv              = (c_ubyte * iv_len)()

        ciphertext      = (c_ubyte * (PlainText_len * 4))()
        password_array  = (c_int * len(password))(*password)

        result          = self.SCrypto.SecureEncrypt(
            plaintext_array, PlainText_len,
            password_array, len(password),
            salt, salt_len,
            self.Params['Iterations'],
            iv, iv_len,
            ciphertext
        )

        if result < 0:
            return b''
        
        return bytes(salt) + bytes(iv) + bytes(ciphertext[:result])

    def get_secure_password(self, FileName: str) -> list[int]:
        Output = (c_int * 128)()
        OutputLen = c_int()
        self.SCrypto.GetSecureKey(FileName.encode("UTF-8"), Output, byref(OutputLen))

        return list(Output[:OutputLen.value])
    
    @classmethod
    def GSP(cls, FileName: str) -> list[int]:
        if not cls.instance:
            raise RuntimeError("Instance does not exist.")

        return cls.instance.get_secure_password(str(FileName))

# Version Globale: v00.00.00.0g
# Version du fichier: v00.00.00.01
