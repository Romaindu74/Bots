import os

class _Label(object):
    def __init__(self, *, text: str = False) -> None:
        self.__text = text

    def __str__(self) -> str:
        return self.__text

    def __len__(self) -> int:
        return len(self.__text)

    def config(self, *, text: str = False) -> None:
        if text:
            self.__text = text

class _LabelFrame(object):
    def __init__(self, *, text: str = False) -> None:
        self.__text = text
        self.elements = []

    def __str__(self) -> str:
        return self.__text

    def __len__(self) -> int:
        return len(self.__text)

    def Add(self, Label: _Label) -> None:
        self.elements.append(Label)

    def Label(self, * , text: str = False) -> _Label:
        Label = _Label(text = text)
        self.elements.append(Label)
        return Label

class Table(object):
    def __init__(self, max_width: int):
        self._max     = max_width
        self.print = True
        self.elements = []

    def LabelFrame(self, text: str = False) -> _LabelFrame:
        LabelFrame = _LabelFrame(text = text)
        self.elements.append(LabelFrame)
        return LabelFrame

    def Label(self, * , text: str = False) -> _Label:
        Label = _Label(text = text)
        self.elements.append(Label)
        return Label

    @property
    def Reload(self) -> None:
        if(os.name == 'posix'):os.system('clear')
        else:os.system('cls')
        self.mainloop()

    def mainloop(self) -> None:
        _str = ""
        for a in self.elements:
            if isinstance(a, _Label):
                _str += '{0}\n'.format(str(a))
            elif isinstance(a, _LabelFrame):
                _str += '|{0}'.format(str(a))
                for b in range(self._max-len(a)-2):_str+="-"
                _str+='|\n'
                for c in a.elements:
                    _str += '|{0}'.format(str(c))
                    for b in range(self._max-len(c)-2):_str+=" "
                    _str += '|\n'
                _str+="|"
                for d in range(self._max-2):_str+="-"
                _str+="|\n"
        if self.print:
            print(_str)
