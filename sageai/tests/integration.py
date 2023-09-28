import json
import os
from time import sleep
from typing import cast, get_type_hints

import pytest
from sageai.types.function import Function

from sageai.types.log_level import LogLevel
from sageai.utils.file_utilities import (
    get_functions_directories,
    load_module_from_file,
)
from sageai.utils.logger import get_logger
from sageai.sageai import SageAI

logger = get_logger(LogLevel.INFO)


@pytest.mark.parametrize(
    "dirpath",
    get_functions_directories(
        logger=logger, functions_directory_path=os.getenv("TEST_DIRECTORY")
    ),
)
def test_integration(dirpath):
    sleep(2)
    test_file = os.path.join(dirpath, "test.json")
    function_file = os.path.join(dirpath, "function.py")
    function_module = load_module_from_file("function.py", function_file)
    function_to_test = cast(Function, getattr(function_module, "function"))

    directory_full_path = os.path.abspath(os.getcwd())
    functions_directory = os.path.join(directory_full_path, dirpath)

    openai_key = os.environ["OPENAI_KEY"]
    sageai = SageAI(openai_key=openai_key, functions_directory=functions_directory)
    sageai.index()

    try:
        output_data_model_class = get_type_hints(function_to_test.function)["return"]

        with open(test_file) as f:
            test_cases = json.load(f)
            for i, test_case in enumerate(test_cases):
                logger.info(
                    f"{function_module.function.name} - Running test case {i}/{len(test_cases)}: {test_case['message']}",
                )
                result = None
                try:
                    results = sageai.chat(
                        messages=[dict(role="user", content=test_case["message"])],
                        model="gpt-3.5-turbo-0613",
                        sageai=dict(k=5),
                    )
                    if results is None:
                        raise Exception("No result returned from Sennin")

                    print("results: ", results)
                    test_output = output_data_model_class(**test_case["output"])
                    print("test_output: ", test_output)

                    try:
                        assert (
                            function_module.function.name in result.potential_functions
                        ), "VectorDB did not return expected function"
                        assert (
                            result.function.name == function_module.function.name
                        ), "Wrong function chosen by model"
                        assert (
                            result.result.data == test_output
                        ), "Expected output does not match actual output"
                    except AssertionError as e:
                        logger.exception(
                            f"Function {function_module.function.name} assertions failed: {str(e)}"
                        )
                        continue
                except Exception as e:
                    logger.exception(
                        f"Function {function_module.function.name} failed: {str(e)}"
                    )
    except Exception as e:
        logger.exception(f"Entire test failed: {str(e)}")
