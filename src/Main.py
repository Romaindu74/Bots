try:
    import Bot
except FileNotFoundError as e:
    raise FileNotFoundError(e)
except Exception as e:
    raise Exception(e)

if not Bot.UpDate().Start():
    Bot.Log(30, 'The update could not be done')

if Bot.Ready:
    Bot.Main()