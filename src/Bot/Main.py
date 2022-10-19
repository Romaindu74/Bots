from .GetLang   import Code
from .Logger    import Logger

_log = Logger(__name__)

from time       import sleep     as sleep
from .Interface import Interface as I
from .Options   import Options   as O

class Main(object):
    def __init__(self, **kwargs) -> None:
        _log.Info(Code('0.0.2.3.2'))
        options = O()

        while not options.Initialized:
            sleep(0.5)
        _log.Info(Code('0.0.2.3.3'))

        _log.Info(Code('0.0.2.3.4'))
        Interface = I(options)
        Interface.start()

        while not Interface.Initialized:
            if not Interface.check:
                _log.Critical(Code('0.0.2.3.5'))
                exit()
            sleep(0.5)
        _log.Info(Code('0.0.2.3.6'))


        _log.Info(Code('0.0.2.3.7'))
        try:
            Interface.Start()
            Interface.join()
        except Exception as e:
            _log.Critical(Code('0.0.2.3.8'))
        else:
            _log.Info(Code('0.0.2.3.9'))