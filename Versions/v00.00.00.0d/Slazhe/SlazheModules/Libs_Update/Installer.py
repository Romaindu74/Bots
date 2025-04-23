from Slazhe import Logger, LogProgressBar

Log = Logger(__name__)

from typing import List, Dict, Any

import subprocess
import importlib
import sys

class InstallerModules:
    def __init__(self, MissingModules: List[Dict[str, Any]]) -> None:
        self.MissingModules: List[Dict[str, Any]] = MissingModules

    def _is_pip_enabled(self) -> bool:
        result = subprocess.run([sys.executable, '-m', 'ensurepip', '--default-pip'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0

    def _install_module(self, module_name: str) -> bool:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', module_name],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0

    def check(self) -> None:
        Log.Debug("Checking if pip is enabled...")
        if not self._is_pip_enabled():
            return Log.Error("pip is not enabled. Please manually missing modules.")
        Log.Debug("pip is enabled.")

        MissingModules = self._find_missing_modules()
        if len(MissingModules) == 0:
            return Log.Info("No missing modules found.")

        progress_bar = LogProgressBar(len(MissingModules))
        Log.Info(f"Installing {", ".join([m.get("pip-name", "Unknown") for m in MissingModules])}...")
        for module in MissingModules:
            if self._install_module(module['pip-name']):
                progress_bar.add(1, 'green')
            else:
                progress_bar.add(1, 'red')
                Log.Error(f"{module.get('pip-name', 'Unknown')} can't be installed.")
            progress_bar.print()

    def _find_missing_modules(self) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []

        for module in self.MissingModules:
            try:
                importlib.import_module(module['import-name'])
            except ImportError:
                result.append(module)

        return result
# Version Globale: v00.00.00.0d
# Version du fichier: v00.00.00.01
