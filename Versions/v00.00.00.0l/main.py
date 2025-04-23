if __name__ != "__main__":
    import sys
    sys.exit(1)

from Slazhe import Logger, LoggerConfig, LogLevels

LoggerConfig.init(FileFormat = 'Log %Y-%m-%d.log', Folder = 'Logs/', Level = LogLevels.INFO)

Log = Logger(__name__)

import time

while not Log.initialised:
    time.sleep(0.25)

import datetime as _dt

Log.Debug(f"The program started on: {_dt.datetime.now()}")

from Slazhe.SlazheModules import importer

import os, sys

from typing import Any

if getattr(importer, "SlazheMain", None):
    SlazheMain = importer.SlazheMain
else:
    Log.Warn("Module Route is not found, skipping checks missing modules.")
    SlazheMain = None

LoggerColorama = sys.modules.get('colorama', False)

# Initial usage of the class
if getattr(importer, "get_modules", None) and SlazheMain:
    MissingModules: list[str] = importer.get_modules(os.getcwd() + os.sep)
    Log.Warn("Missing modules is:", ", ".join(MissingModules))

    Modules: list[dict[str, Any]] = SlazheMain.get_modules()

    InstallingModules: list[dict[str, Any]] = []
    for module in Modules:
        if module.get('import-name', 'Unknown') in MissingModules:
            InstallingModules.append(module)
            Log.Info(f"Module {module.get('import-name', 'Unknown')} is missing, and it will be installed.")
        elif module.get('required', False):
            InstallingModules.append(module)

    Installer = importer.InstallerModules(InstallingModules)
    # Installer.check()

    if not LoggerColorama:
        Log.reload()

    Log.Info("Modules checked successfully.")   

SlazheCrypto = getattr(importer, "SlazheCrypto", False)
if not SlazheCrypto:
    Log.Warn("SlazheCrypto is not available.")
else:
    Crypto = importer.SlazheCrypto()
    Crypto.config()

from Slazhe.Modules import importer as module_importer

if getattr(importer, 'GlobalVars', None):
    GlobalVars = importer.GlobalVars()
    GlobalVars.set_variable("importer", importer)
    GlobalVars.set_variable("module_importer", module_importer)

if getattr(module_importer, 'MainCli', None):
    MainCli = module_importer.MainCli()











    # from Slazhe.core.Bots import SlazheBot

    # Bot = SlazheBot("testtests")

    # def SlazheBotStart(Bot: SlazheBot) -> bool:
    #     Bot._running = True
    #     Bot.start()

    #     Bot._botstarted = True

    #     while Bot._botstarted:
    #         time.sleep(0.25)
    #     return not Bot._started_error

    # from Slazhe.modules.discord.commands import setup
    # # from Slazhe.modules.discord.commands.Default import setup
    # # dtest(Bot)
    # setup(Bot)

    # print(SlazheBotStart(Bot), "Ok")

    # Bot.join()


# Version Globale: v00.00.00.0l
# Version du fichier: v00.00.00.01
