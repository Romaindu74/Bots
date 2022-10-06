from .UpDate import UpDate
from .Logger import Log

Ready = False
try:
    from .Main import Main
    Ready = True
except Exception as e:
    raise Exception(str(e))