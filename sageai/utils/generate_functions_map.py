import importlib
from logging import Logger
import os
from types import ModuleType
from typing import List, Optional
from sageai.types.function import Function
from sageai.utils.logger import get_logger


def find_parent_with_child(start_path, target_child_name):
    current_path = os.path.abspath(start_path)

    while current_path != os.path.dirname(current_path):
        potential_child_path = os.path.join(current_path, target_child_name)
        if os.path.isdir(potential_child_path):
            return current_path
        current_path = os.path.dirname(current_path)

    raise Exception("Can't find project root directory.")


def load_module_from_file(filename: str, filepath: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(filename, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_functions_directories(
    logger: Logger,
    functions_directory_path: str = None,
) -> List[str]:
    logger.info(
        f"Getting functions directories from {functions_directory_path}",
    )

    for dirpath, dirnames, filenames in os.walk(functions_directory_path):
        print("---\ndirpath: ", dirpath)
        print("dirnames: ", dirnames)
        print("filenames: ", filenames)

    function_directories = [
        dirpath
        for dirpath, dirnames, filenames in os.walk(functions_directory_path)
        if "function.py" in filenames
    ]
    logger.info(f"Found {len(function_directories)} function directories")
    return sorted(function_directories)


def generate_functions_map(functions_directory_path: str) -> dict[str, Function]:
    logger = get_logger()
    available_functions = {}

    logger.info("Generating function map")
    functions_directory = get_functions_directories(logger, functions_directory_path)

    logger.info("functions_directory", extra={"asd": functions_directory})
    for dirpath in functions_directory:
        folder_name = os.path.basename(dirpath)
        function_file = os.path.join(dirpath, "function.py")
        function_module = load_module_from_file(folder_name, function_file)

        if not hasattr(function_module, "function"):
            raise Exception(
                f"Function {folder_name} does not have a function attribute",
            )

        available_functions[function_module.function.name] = function_module.function

    if len(available_functions) == 0:
        raise Exception("No functions found")
    logger.info(f"Function map generated with {len(available_functions)} functions")
    available_functions = dict(sorted(available_functions.items()))
    return available_functions
