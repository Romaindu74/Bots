from Slazhe import Logger

Log = Logger(__package__)

from typing import Dict, Any

from .Question      import Page, PageManager, QuestionPage
from .BaseCliModule import SlazheCliModule

from rich.table     import Table

class CliShowModules(SlazheCliModule):
    """
    CLI module to show and manage loaded modules.
    """

    def get_modules(self) -> Dict[str, Any]:
        """
        Retrieve the loaded modules.

        Returns:
            Dict[str, Any]: A dictionary of module names and their corresponding objects.
        """
        from Slazhe.SlazheModules import importer

        if not hasattr(importer, 'GlobalVars'):
            Log.Error("Global variables not available.")
            return {}

        GlobalVars  = importer.GlobalVars()
        main_importer   = GlobalVars.get_variable('importer', {})
        module_importer = GlobalVars.get_variable('module_importer', {})

        modules = {**getattr(main_importer, 'imported_modules', {}),
                   **getattr(module_importer, 'imported_modules', {})}

        return modules

    def get_table_modules(self, modules: Dict[str, Any]) -> Table:
        """
        Create a table of modules.

        Args:
            modules (Dict[str, Any]): A dictionary of module names and their corresponding objects.

        Returns:
            Table: A Rich Table object containing the modules.
        """
        table = Table(width=self.console.width)
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Module", style="magenta")

        for key, value in modules.items():
            table.add_row(key, str(value))

        Log.Debug("Table of modules created.")
        return table

    def print_modules(self) -> None:
        """
        Print the table of modules.
        """
        modules = self.get_modules()

        if not modules:
            self.quit = True
            Log.Warning("No modules found.")
            return

        table = self.get_table_modules(modules)
        self.console.print(table)
        Log.Debug("Modules table printed.")

    def reload_module(self, module: str, force: bool = False) -> None:
        """
        Reload a specific module.

        Args:
            module (str): The name of the module to reload.
            force (bool): Whether to force reload the module.
        """
        modules = self.get_modules()

        if module not in modules:
            Log.Warning(f"Module '{module}' does not exist.")
            return self.parent.error(f"Le module '{module}' n'existe pas.")

        if force:
            self.force_reload_module(module)
        else:
            self.standard_reload_module(modules[module], module)

    def standard_reload_module(self, module: Any, module_name: str) -> None:
        """
        Standard reload of a module.

        Args:
            module (Any): The module object to reload.
            module_name (str): The name of the module.
        """
        if not hasattr(module, 'reload'):
            Log.Warning(f"Module '{module_name}' does not have a reload function.")
            return self.parent.error(f"Le module '{module_name}' ne possède pas de fonction de rechargement.")

        try:
            module.reload()
            Log.Info(f"Module '{module_name}' reloaded successfully.")
        except Exception as e:
            Log.Error(f"Error reloading module '{module_name}': {e}")

    def force_reload_module(self, module: str) -> None:
        """
        Force reload a specific module.

        Args:
            module (str): The name of the module to force reload.
        """
        from Slazhe.SlazheModules import importer

        if not hasattr(importer, 'GlobalVars'):
            Log.Error("Global variables not available.")
            return

        GlobalVars = importer.GlobalVars()
        saved_variables = GlobalVars.save_variables()

        for importer_name in ['importer', 'module_importer']:
            importer_instance = GlobalVars.get_variable(importer_name, {})
            importer_modules = getattr(importer_instance, 'imported_modules', {})

            if module in importer_modules:
                self.unload_and_reload_module(importer_modules, module, importer_instance)

        GlobalVars.restore_variables(saved_variables)
        Log.Info(f"Module '{module}' force reloaded successfully.")

    def unload_and_reload_module(self, importer_modules: Dict[str, Any], module: str, importer_instance: Any) -> None:
        """
        Unload and reload a module.

        Args:
            importer_modules (Dict[str, Any]): The dictionary of imported modules.
            module (str): The name of the module to unload and reload.
            importer_instance (Any): The importer instance.
        """
        try:
            if hasattr(importer_modules[module], 'unload'):
                importer_modules[module].unload()
        except Exception as e:
            Log.Error(f"Error stopping module '{module}': {e}")

        importer_instance.reload_module(module)

        try:
            callback = getattr(importer_instance, 'imported_modules', {}).get(module)
            if callback and hasattr(callback, 'load'):
                callback.load()
        except Exception as e:
            Log.Error(f"Error starting module '{module}': {e}")

    def run(self) -> None:
        """
        Run the module management loop.
        """
        self.quit = False

        pages = [
            Page("Menu", 1, self.parent_run),
            Page("Recharger le tableau", 2, self.print_modules),
            Page("Recharger un module", 3, self.reload_module, [QuestionPage("Entrez le nom du module à recharger", variable = "module", console = self.console, prompt = self.prompt)], attrs = { "force": True }),
        ]

        page_manager = PageManager(pages, console=self.console, prompt=self.prompt)

        self.print_modules()
        while not self.quit:
            page_manager.run()

    def parent_run(self) -> None:
        """
        Return to the parent CLI loop.
        """
        self.quit = True

# Version Globale: v00.00.00.0h
# Version du fichier: v00.00.00.01
