from Slazhe import Logger

Log = Logger(__package__)

def MainCli():
    from .Libs_cli.Home import SlazheCli

    Log.Info("Starting Slazhe CLI.")
    SlazheCli().run()

def unload():
    from .Libs_cli.Home import SlazheCli

    SlazheCli().stop = True
    SlazheCli()._instance = None

def load():
    MainCli()
# Version Globale: v00.00.00.0c
# Version du fichier: v00.00.00.01
