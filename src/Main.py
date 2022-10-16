try:
    import Bot
except FileNotFoundError as e:
    raise FileNotFoundError(e)
except Exception as e:
    raise Exception(e)

_log = Bot.Logger(__name__)

_log.Info('Verification des mise a jour')
if not Bot.UpDate().Start():
    _log.Error('The update could not be done')

_log.Info('Lancement du programe')
if Bot.Ready:
    Bot.Main()
else:
    _log.Critical('Le programe n\' es pas pret')