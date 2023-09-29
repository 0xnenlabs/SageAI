import json
import os
from time import sleep
from typing import cast, get_type_hints
import pydantic

import pytest

from sageai.sageai import SageAI
from sageai.types.function import Function
from sageai.types.log_level import LogLevel
from sageai.utils.file_utilities import get_functions_directories, load_module_from_file
from sageai.utils.logger import get_logger

logger = get_logger("IntegrationTest", LogLevel.INFO)


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
    function_module = load_module_from_file("function", function_file)
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
                    f"{function_module.function.name} - Running test case {i+1}/{len(test_cases)}: {test_case['message']}",
                )
                try:
                    vector_db_result = sageai.vectordb.search(
                        query=test_case["message"], top_n=5
                    )
                    result = sageai.chat(
                        messages=[dict(role="user", content=test_case["message"])],
                        model="gpt-3.5-turbo-0613",
                        top_n=5,
                    )
                    if result is None:
                        logger.error(
                            "No result returned from Sennin for function: {}".format(
                                function_module.function.name
                            )
                        )
                        continue

                    test_output = None
                    try:
                        test_output = output_data_model_class(
                            **test_case["output"]
                        ).dict()
                    except pydantic.ValidationError as ve:
                        expected_fields = ", ".join(
                            get_type_hints(output_data_model_class).keys()
                        )
                        actual_fields = test_case["output"]
                        logger.error(
                            f"Validation error for function output {function_module.function.name}:\nExpected fields: {expected_fields}\nGot: {actual_fields}.\n{str(ve)}"
                        )
                        continue

                    if function_module.function.name not in vector_db_result:
                        logger.error(
                            f"VectorDB did not return expected function for {function_module.function.name}. Expected: {function_module.function.name} in {vector_db_result}."
                        )
                        continue
                    if result["name"] != function_module.function.name:
                        logger.error(
                            f"Wrong function chosen by model for {function_module.function.name}. Expected: {function_module.function.name}, Got: {result['name']}"
                        )
                        continue
                    if result["result"] != test_output:
                        logger.error(
                            f"Output mismatch for {function_module.function.name}. Expected: {test_output}, Got: {result['result']}"
                        )
                        continue

                except Exception as e:
                    logger.error(
                        f"Function {function_module.function.name} execution failed: {str(e)}"
                    )

    except Exception as e:
        logger.error(f"Entire test failed: {str(e)} for directory {dirpath}")
