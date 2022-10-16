from .type.Cog      import Setup
from .type.Bot      import Bot

from .GetLang       import Get_Lang
from .Logger        import Logger

from .Utils         import MISSING

import os, importlib

_log = Logger(__name__)

async def AddCog(Bot: Bot = MISSING) -> bool:
    if Bot == MISSING:
        _log.Warn('Bot Missing')
        return False

    _log.Info('Recuperation des cogs')
    cogs:    list[str] = [f for f in os.listdir('Bot/Cog/') if os.path.isfile(os.path.join('Bot/Cog/', f))]
    modules: bool      = True
    _log.Info('Recuperation des cogs Fait')

    for cog in cogs:
        try:
            _log.Info('Chargement du module {0}'.format(cog.replace('.py', '')))
            module: Setup = importlib.import_module('.'+cog.replace('.py', ''), 'Bot.Cog')

            if not await module.setup(Bot):
                _log.Warn(Get_Lang.get('0.0.1.4.7').format(name = cog))
                modules = False

        except Exception as e:
            _log.Error(Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)))

        else:
            _log.Info('Chargement du module {0} reussi'.format(cog.replace('.py', '')))

    if modules:
        _log.Info(Get_Lang.get('0.0.1.4.8'))

    return True