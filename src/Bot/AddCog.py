from .type.Cog      import Setup
from .type.Bot      import Bot

from .GetLang       import Code
from .Logger        import Logger

from .Utils         import MISSING

import os, importlib

_log = Logger(__name__)

async def AddCog(Bot: Bot = MISSING) -> bool:
    if Bot == MISSING:
        _log.Warn(Code('0.0.0.9.3'))
        return False

    _log.Info(Code('0.0.0.9.4'))
    cogs:    list[str] = [f for f in os.listdir('Bot/Cog/') if os.path.isfile(os.path.join('Bot/Cog/', f))]
    modules: bool      = True
    _log.Info(Code('0.0.0.9.5'))

    for cog in cogs:
        try:
            _log.Info('Chargement du module {0}'.format(cog.replace('.py', '')))
            module: Setup = importlib.import_module('.'+cog.replace('.py', ''), 'Bot.Cog')

            if not await module.setup(Bot):
                _log.Warn(Code('0.0.1.4.7').format(cog = cog))
                modules = False

        except Exception as e:
            _log.Error(Code('0.0.0.0.1').format(file = __file__, error = str(e)))

        else:
            _log.Info(Code('0.0.0.9.7').format(cog = cog.replace('.py', '')))

    if modules:
        _log.Info(Code('0.0.0.9.8'))

    return True