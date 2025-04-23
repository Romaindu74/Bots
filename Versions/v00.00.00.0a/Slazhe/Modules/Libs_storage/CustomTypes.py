from typing import Callable, Any

class EBase:
    SlazheStorageFile: Callable

    def __init__(self, value: Any):
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

# Sous-classes des types natifs
class EDict(dict, EBase): pass
class EInt(int, EBase): pass
class EFloat(float, EBase): pass
class EComplex(complex, EBase): pass
class EList(list, EBase): pass
class ETuple(tuple, EBase): pass
class ERange(EBase):
    def __init__(self, value: range):
        super().__init__(value)

class EStr(str, EBase): pass
class ESet(set, EBase): pass
class EFrozenSet(frozenset, EBase): pass
class EBytes(bytes, EBase): pass
class EByteArray(bytearray, EBase): pass
class EMemoryView(EBase):
        def __init__(self, value: memoryview):
            super().__init__(value)
class EBool(EBase):
        def __init__(self, value: bool):
            super().__init__(value)
class ENoneType(EBase):
    def __init__(self, value=None):
        super().__init__(value)

CustomTyping: dict[str, Callable[[Any], EBase]] = {
    "memoryview":   EMemoryView,
    "frozenset":    EFrozenSet,
    "bytearray":    EByteArray,
    "NoneType": ENoneType,
    "complex":  EComplex,
    "float":    EFloat,
    "tuple":    ETuple,
    "range":    ERange,
    "bytes":    EBytes,
    "list": EList,
    "bool": EBool,
    "dict": EDict,
    "int":  EInt,
    "str":  EStr,
    "set":  ESet,
}

def to_extended(data) -> EBase:
    T = type(data).__name__  # Récupère le nom du type en tant que chaîne
    if T not in CustomTyping:
        raise ValueError(f"Type '{T}' non pris en charge.")
    return CustomTyping[T](data)

# Version Globale: v00.00.00.0a
# Version du fichier: v00.00.00.01
