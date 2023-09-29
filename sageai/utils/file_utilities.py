import os
from importlib import util
from types import ModuleType
from typing import List

from sageai.types.function import Function
from sageai.utils.logger import get_logger


def load_module_from_file(module_name: str, filepath: str) -> ModuleType:
    spec = util.spec_from_file_location(module_name, filepath)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_functions_directories(
    logger,
    functions_directory_path: str = None,
) -> List[str]:
    logger.info(
        f"Getting functions directories from {functions_directory_path}",
    )

    function_directories = [
        dirpath
        for dirpath, dirnames, filenames in os.walk(functions_directory_path)
        if "function.py" in filenames
    ]
    logger.info(f"Found {len(function_directories)} function directories")
    return sorted(function_directories)


def generate_functions_map() -> dict[str, Function]:
    from sageai.config import get_config

    config = get_config()
    functions_directory_path = config.functions_directory
    log_level = config.log_level
    logger = get_logger("Utils", log_level)
    available_functions = {}

    logger.info("Generating function map")
    functions_directory = get_functions_directories(logger, functions_directory_path)

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
