import json
import os
from time import sleep

import pytest
from lasso_sennin.common.types.lasso.Metadata import Query, SenninMetadata, User
from lasso_sennin.sennin.sennin import Sennin
from lasso_sennin.utils.file_utilities import (
    append_json,
    get_function_directories,
    load_module_from_file,
)
from lasso_sennin.utils.logger import Logger
from lasso_sennin.utils.model_utilities import get_output_data_model

logger = Logger("IntegrationTests")


@pytest.mark.parametrize(
    "dirpath",
    get_function_directories(logger=logger, test_directory=os.getenv("TEST_DIRECTORY")),
)
def test_integration(dirpath):
    sleep(2)
    log_timestamp = os.getenv("LOG_TIMESTAMP")
    integration_file = f"logs/{log_timestamp}/integration.json"

    test_file = os.path.join(dirpath, "test.json")
    types_file = os.path.join(dirpath, "types.py")
    function_file = os.path.join(dirpath, "function.py")
    function_module = load_module_from_file("function.py", function_file)

    try:
        sennin_metadata = SenninMetadata(
            user=User(
                id="USER#123",
                discord_username="@DISCORD_USERNAME",
            ),
            query=Query(
                id="query#123",
            ),
        )
        sennin = Sennin(metadata=sennin_metadata)
        types_module = load_module_from_file("types", types_file)
        output_data_model_class = get_output_data_model(module=types_module)

        with open(test_file) as f:
            test_cases = json.load(f)
            for i, test_case in enumerate(test_cases):
                logger.info(
                    f"{function_module.function.name} - Running test case {i}/{len(test_cases)}: {test_case['message']}",
                )
                result = None
                try:
                    results = sennin.run_message(
                        message=test_case["message"],
                        keyword_map=None,
                    )
                    if results is None:
                        raise Exception("No result returned from Sennin")
                    result = results[0]
                    if result.result.error:
                        append_json(
                            function_module.function.name,
                            {
                                "Test index": i,
                                "Test message": test_case["message"],
                                "Expected function": function_module.function.name,
                                "Expected input": test_case["input"],
                                "Expected output": test_case["output"],
                                "Vector DB output": result.potential_functions,
                                "Actual function": result.function.name,
                                "Actual input": json.loads(
                                    result.parameters.json(),
                                ),
                                "Actual output": None,
                                "Error": result.result.error,
                            },
                            integration_file,
                        )
                        continue

                    # only show first 3 rows
                    if getattr(result.result.data, "rows", None):
                        result.result.data.rows = result.result.data.rows[:3]

                    test_output = output_data_model_class(**test_case["output"])

                    integration_data = {
                        "Test index": i,
                        "Test message": test_case["message"],
                        "Expected function": function_module.function.name,
                        "Expected input": test_case["input"],
                        "Expected output": test_case["output"],
                        "Vector DB output": result.potential_functions,
                        "Actual function": result.function.name,
                        "Actual input": json.loads(result.parameters.json()),
                        "Actual output": json.loads(result.result.data.json()),
                        "Error": None,
                    }

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
                        integration_data["Error"] = str(e)
                        append_json(
                            function_module.function.name,
                            integration_data,
                            integration_file,
                        )
                        continue

                    append_json(
                        function_module.function.name,
                        integration_data,
                        integration_file,
                    )
                except Exception as e:
                    integration_data = {
                        "Test index": i,
                        "Test message": test_case["message"],
                        "Expected function": function_module.function.name,
                        "Expected input": test_case["input"],
                        "Expected output": test_case["output"],
                        "Vector DB output": result.potential_functions
                        if result
                        else None,
                        "Actual function": result.function.name if result else None,
                        "Actual input": json.loads(result.parameters.json())
                        if result
                        else None,
                        "Actual output": json.loads(result.result.data.json())
                        if result
                        else None,
                        "Error": str(e),
                    }
                    append_json(
                        function_module.function.name,
                        integration_data,
                        integration_file,
                    )
    except Exception as e:
        append_json(
            function_module.function.name,
            {"Error": "Entire test failed because:" + str(e)},
            integration_file,
        )
