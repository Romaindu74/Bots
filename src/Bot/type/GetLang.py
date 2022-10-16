from typing import Union

class Get_Lang:
    def get(self, code: str = False, __default: str = False, **options) -> Union[str, bool, None]:...

class Get_User_Lang:
    get_lang: str

    def __init__(self, id: int, Lang: str = False)    -> None:...
    def get(self, __key: str, __default: str = False) -> Union[str, bool, None]:...