from typing import Dict, Any, Iterator, Callable

import importlib
import pkgutil
import inspect
import os
import sys

class DynamicImporter:
    def __getattr__(self, name: str) -> Callable: ...

    def __init__(self, package_name: str, path: str) -> None:
        """
        Initialize the DynamicImporter with the given package name.

        Args:
            package_name (str): The name of the package to import from.
        """
        self.package_name = package_name
        self.path: str    = path
        self.imported_modules: Dict[str, Any] = {}
        self.imported_attributes: Dict[str, Any] = {}

    def get_current_directory(self) -> str:
        """Get the current directory path."""
        return os.path.dirname(self.path)

    def get_module_info(self, directory: str) -> Iterator[pkgutil.ModuleInfo]:
        """Get the module information for the given directory."""
        return pkgutil.iter_modules([directory])

    def is_package(self, module_info: pkgutil.ModuleInfo) -> bool:
        """Check if the given module information represents a package."""
        return module_info.ispkg

    def import_module(self, module_name: str) -> Any:
        """Import the module with the given name."""
        return importlib.import_module(f'{self.package_name}.{module_name}', package=self.package_name)

    def is_class_or_function(self, attr: Any) -> bool:
        """Check if the given attribute is a class or a function."""
        return inspect.isclass(attr) or inspect.isfunction(attr)

    def import_attributes(self, module: Any) -> None:
        """Import all classes and functions from the given module."""
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if self.is_class_or_function(attr):
                self.imported_attributes[attr_name] = attr
                setattr(self, attr_name, attr)  # Stocker directement dans self.__dict__

    def import_all_classes_and_functions(self) -> None:
        """Import all classes and functions from all modules in the current directory."""
        current_dir = self.get_current_directory()
        for module_info in self.get_module_info(current_dir):
            if self.is_package(module_info):
                continue  # Skip sub-packages

            module_name = module_info.name
            module = self.import_module(module_name)
            self.imported_modules[module_name] = module
            self.import_attributes(module)

    def reload_module(self, module_name: str) -> None:
        for key in list(sys.modules.keys()):
            if f"{self.package_name}" in key:
                del sys.modules[key]

        new_module = importlib.import_module(f"{self.package_name}.{module_name}", package=self.package_name)

        self.imported_modules[module_name] = new_module
        self.import_attributes(new_module)

    def reload_modules(self) -> None:
        """Reload all imported modules and re-import their attributes."""
        for module_name in list(self.imported_modules.keys()):
            self.reload_module(module_name) 

    def reload_class_or_function(self, name: str) -> None:
        """Reload only the module that contains the specified class or function.

        Args:
            name (str): The name of the class or function to reload.
        """
        for module_name, module in self.imported_modules.items():
            if hasattr(module, name):  # Vérifie si la classe/fonction est définie dans ce module
                self.reload_module(module_name)  # Recharge le module
                setattr(self, name, getattr(module, name))  # Met à jour la référence
                return

        raise ValueError(f"'{name}' not found in imported modules.")


# Version Globale: v00.00.00.0m
# Version du fichier: v00.00.00.01
