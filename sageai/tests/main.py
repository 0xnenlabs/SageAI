import argparse
import os

import pytest


def main():
    parser = argparse.ArgumentParser(description="Run tests for a specified function.")
    parser.add_argument("--function", type=str, help="Name of function to test")
    args = parser.parse_args()

    if args.function:
        os.environ["TEST_DIRECTORY"] = args.function

    pytest.main(["-x", "-s", "sageai/tests/unit.py"])
    # pytest.main(["-x", "-s", "sageai/tests/integration.py"])
