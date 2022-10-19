from .UpDate    import UpDate
from .Logger    import Log, Logger
from .GetLang   import Code

_log = Logger(__name__)

Ready = False
try:
    _log.Info(Code('0.0.0.9.1'))
    from .Main  import Main
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = e))
    raise Exception(str(e))
else:
    Ready = True
    _log.Info(Code('0.0.0.9.2'))
