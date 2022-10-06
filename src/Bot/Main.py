from .Interface import Interface as I
from .Options   import Options   as O

class Main(object):
    def __init__(self, **kwargs) -> None:
        options = O()

        while not options.Initialized:
            pass

        Interface = I(options)
        Interface.start()

        while not Interface.Initialized:
            if not Interface.check:
                exit()

        Interface.Start()

        Interface.join()