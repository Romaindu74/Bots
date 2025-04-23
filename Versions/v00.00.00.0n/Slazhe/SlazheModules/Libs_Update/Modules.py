from Slazhe import Logger, LogProgressBar

Log: Logger = Logger(__name__)

from typing import List, Dict, Set

import importlib
import warnings
import ast
import os

def check_local_import(root: str, import_name: str) -> bool:
    """
    Check if the import is a local module.

    Args:
        root (str): The root directory of the project.
        import_name (str): The name of the module to import.

    Returns:
        bool: True if the import is a local module, False otherwise.
    """
    import_path: str = os.path.join(root, import_name)

    if os.path.exists(import_path + ".py") or os.path.exists(os.path.join(import_path, "__init__.py")):
        return True

    return False

def check_local_from_import(root: str, import_name: str, level: int) -> bool:
    """
    Check if the import from is a local module.

    Args:
        root (str): The root directory of the project.
        import_name (str): The name of the module to import.
        level (int): The level of the relative import.

    Returns:
        bool: True if the import from is a local module, False otherwise.
    """
    if level > 1:
        import_path: str = os.path.join(os.sep.join(root.split(os.sep)[:-(level - 1)]), import_name.replace(".", os.sep))
    else:
        import_path: str = os.path.join(root, import_name.replace(".", os.sep))

    if os.path.exists(import_path + ".py") or os.path.exists(os.path.join(import_path, "__init__.py")) or os.path.exists(import_path):
        return True

    return False

def extract_modules(root: str, file_name: str) -> Set[str]:
    """
    Extract the list of imported modules from a Python file.

    Args:
        root (str): The root directory of the project.
        file_name (str): The name of the file to analyze.

    Returns:
        Set[str]: A set of imported modules.
    """
    file_path: str = os.path.join(root, file_name)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                tree = ast.parse(file.read(), filename=file_path)
                if w:
                    for warning in w:
                        Log.Warn("SyntaxWarning in file:", file_path)
                        Log.Warn("Warning message:", warning.message)
    except Exception as e:
        Log.Error("Failed to read file:", file_path)
        Log.Error("Exception:", e)
        return set()

    imports: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if check_local_import(root, alias.name):
                    continue

                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                if check_local_from_import(root, node.module, node.level):
                    continue

                imports.append(node.module.split(".")[0])

    return set(imports)

def create_module_map(project_directory: str) -> Dict[str, str]:
    """
    Create a map of modules to their file paths.

    Args:
        project_directory (str): The root directory of the project.

    Returns:
        Dict[str, str]: A dictionary mapping module names to their file paths.
    """
    total_files = sum(1 for root, dirs, files in os.walk(project_directory) for file in files if file.endswith('.py'))
    progress_bar = LogProgressBar(total_files)

    module_map: Dict[str, str] = {}

    Log.Info("Module map creating...")

    for root, dirs, files in os.walk(project_directory):
        for file in files:
            if not file.endswith('.py'):
                continue

            for _import in extract_modules(root, file):
                module_map[_import] = os.path.join(root, file)

            progress_bar.add(1, "green")
            progress_bar.print()

    Log.Info("Module map created with", len(module_map), "entries.")

    return module_map

def find_missing_modules(project_directory: str) -> List[Dict[str, str]]:
    """
    Check if the imported modules exist in the current environment or are local modules.

    Args:
        project_directory (str): The root directory of the project.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing the file paths and names of missing modules.
    """
    module_map = create_module_map(project_directory)
    progress_bar = LogProgressBar(len(module_map.keys()))

    Log.Info("Checking for missing modules...")

    missing_modules: List[Dict[str, str]] = []
    for module in module_map.keys():
        try:
            importlib.import_module(module)
            progress_bar.add(1, "green")
        except ImportError:
            missing_modules.append(module)
            progress_bar.add(1, "red")
        except Exception:
            progress_bar.add(1, "red")

        progress_bar.print()

    Log.Warn(len(missing_modules), "Missing modules.")

    return missing_modules

def get_modules(directory: str) -> None:
    """
    Print the list of missing modules in the project.

    Args:
        directory (str): The root directory of the project.
    """
    return find_missing_modules(directory)
# Version Globale: v00.00.00.0n
# Version du fichier: v00.00.00.01
