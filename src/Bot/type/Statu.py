try:
    import tkinter as tk
except:
    raise

class Statu_:
    Activity: str
    Text: str
    Statu: str
    Time: int
    Is_Config: bool
    def UpDate_Ping(self, ms: float) -> None:...
    def Interface(self, Activite: tk.Label, Statu: tk.Label, Time: tk.Label, Ping: tk.Label) -> None:...
    def Start(self) -> None:...
    def Stop(self) -> None:...