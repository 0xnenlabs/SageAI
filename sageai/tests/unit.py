import json
import os
from typing import cast, get_type_hints
import pydantic

import pytest

from sageai.types.function import Function
from sageai.types.log_level import LogLevel
from sageai.utils.file_utilities import get_functions_directories, load_module_from_file
from sageai.utils.logger import get_logger

logger = get_logger("UnitTest", LogLevel.INFO)


def assert_function_module_correct(folder_name, function_module):
    if not hasattr(function_module, "function"):
        msg = f"{folder_name}/function.py does not export a variable called 'function'"
        raise ValueError(msg)


def assert_test_cases_correct(test_cases, folder_name):
    for idx, test_case in enumerate(test_cases):
        if not isinstance(test_case, dict):
            msg = f"Test case #{idx + 1} in {folder_name}/test.json is not an object"
            raise ValueError(msg)

        missing_properties = [
            prop for prop in ["input", "output", "message"] if prop not in test_case
        ]
        if missing_properties:
            msg = f"Test case #{idx + 1} in {folder_name}/tests.json missing properties: {', '.join(missing_properties)}"
            raise ValueError(msg)

        if not isinstance(test_case.get("message", ""), str):
            msg = f"Test case #{idx + 1} in {folder_name}/tests.json has a 'message' property which is not of type string"
            raise ValueError(msg)


@pytest.mark.parametrize(
    "dirpath",
    get_functions_directories(
        logger, functions_directory_path=os.getenv("TEST_DIRECTORY")
    ),
)
def test_unit(dirpath):
    folder_name = os.path.basename(dirpath)
    function_file = os.path.join(dirpath, "function.py")
    test_file = os.path.join(dirpath, "test.json")

    try:
        # Check necessary files
        if not os.path.exists(function_file):
            msg = f"Missing function.py in {folder_name}"
            raise ValueError(msg)

        if not os.path.exists(test_file):
            msg = f"Missing test.json in {folder_name}"
            raise ValueError(msg)

        function_module = load_module_from_file("function", function_file)
        function_to_test = cast(Function, getattr(function_module, "function"))
        assert_function_module_correct(folder_name, function_module)

        input_model_class = function_to_test.input_type
        output_data_model_class = get_type_hints(function_to_test.function)["return"]

        with open(test_file) as f:
            test_cases = json.load(f)
            assert_test_cases_correct(test_cases, folder_name)

            for test_case in test_cases:
                logger.info(f"Running message {test_case['message']}")
                func_output = function_to_test(input_model_class(**test_case["input"]))

                test_output = None
                try:
                    test_output = output_data_model_class(**test_case["output"]).dict()
                except pydantic.ValidationError as ve:
                    expected_fields = ", ".join(
                        get_type_hints(output_data_model_class).keys()
                    )
                    actual_fields = test_case["output"]
                    logger.error(
                        f"Validation error for function output {function_module.function.name}:\nExpected fields: {expected_fields}\nGot: {actual_fields}.\n{str(ve)}"
                    )
                    continue

                if func_output != test_output:
                    logger.error(
                        f"Function {folder_name} output mismatch for message '{test_case['message']}':"
                    )
                    logger.error(f"Expected: {test_output}")
                    logger.error(f"Got: {func_output}")
                    raise AssertionError("Expected output does not match actual output")

    except Exception as e:
        logger.error(f"Function {folder_name} failed. Error: {str(e)}")
