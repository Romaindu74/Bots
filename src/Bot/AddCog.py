from .type.Commands import setup
from .type.Bot      import Bot

from .GetLang       import Get_Lang
from .Logger        import Log

from .Utils         import MISSING

import os, importlib

async def AddCog(Bot: Bot = MISSING) -> bool:
    if Bot == MISSING:
        return False

    cogs:    list = [f for f in os.listdir('Bot/Cog/') if os.path.isfile(os.path.join('Bot/Cog/', f))]
    modules: bool = True

    for cog in cogs:
        try:
            module: setup = importlib.import_module('.'+cog.replace('.py', ''), 'Bot.Cog')

            if not await module.setup(Bot):
                Log(30, Get_Lang.get('0.0.1.4.7').format(name = cog))
                modules = False

        except Exception as e:
            Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)))

    if modules:
        Log(20, Get_Lang.get('0.0.1.4.8'))

    return True