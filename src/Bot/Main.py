from .Logger import Logger

_log = Logger(__name__)

from .Interface import Interface as I
from .Options   import Options   as O

class Main(object):
    def __init__(self, **kwargs) -> None:
        _log.Info('Initialisation des options')
        options = O()

        while not options.Initialized:
            pass
        _log.Info('Initialisation des options reussi')

        _log.Info('Initialisation de l\'interface')
        Interface = I(options)
        Interface.start()

        while not Interface.Initialized:
            if not Interface.check:
                _log.Critical('Initialisation des l\'interface failled')
                exit()
        _log.Info('Initialisation des l\'interface reussi')


        _log.Info('Demarage de l\'interface')
        try:
            Interface.Start()
            Interface.join()
        except Exception as e:
            _log.Critical('Demarage de l\'interface failled')
        else:
            _log.Info('Demarage de l\'interface reussi')