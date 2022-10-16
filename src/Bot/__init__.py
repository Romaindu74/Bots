from .UpDate import UpDate
from .Logger import Log, Logger

_log = Logger(__name__)

Ready = False
try:
    _log.Info('Chargement du module principale')
    from .Main import Main
except Exception as e:
    _log.Critical('Un erreur est survenue lors du chargement du module principale\nErreur {0}'.format(e))
    raise Exception(str(e))
else:
    Ready = True
    _log.Info('Chargement du module principale reussi')
