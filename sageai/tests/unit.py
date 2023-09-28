import json
import os
from typing import cast, get_type_hints

import pytest

from sageai.types.function import Function
from sageai.types.log_level import LogLevel
from sageai.utils.file_utilities import get_functions_directories, load_module_from_file
from sageai.utils.logger import get_logger

logger = get_logger(LogLevel.INFO)


def assert_function_module_correct(folder_name, function_module):
    assert hasattr(
        function_module, "function"
    ), f"{folder_name}/function.py does not export a variable called 'function'"


def assert_test_cases_correct(test_cases, folder_name):
    for test_case in test_cases:
        assert isinstance(
            test_case, dict
        ), f"Test case in {folder_name}/test.json is not an object"
        assert (
            "input" in test_case
        ), f"Test case in {folder_name}/tests.json does not have an 'input' property"
        assert (
            "output" in test_case
        ), f"Test case in {folder_name}/tests.json does not have an 'output' property"
        assert "message" in test_case and isinstance(
            test_case["message"], str
        ), f"Test case in {folder_name}/tests.json does not have a 'message' property of type string"


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
        assert os.path.exists(function_file), f"Missing function.py in {folder_name}"
        assert os.path.exists(test_file), f"Missing test.json in {folder_name}"

        function_module = load_module_from_file("function.py", function_file)
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
                test_output = output_data_model_class(**test_case["output"])
                assert (
                    func_output == test_output
                ), "Expected output does not match actual output"

    except Exception as e:
        logger.exception(f"Function {folder_name} failed: {str(e)}")
