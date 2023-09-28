import argparse
import os

import pytest


def main():
    parser = argparse.ArgumentParser(description="Run tests for functions.")
    parser.add_argument("--directory", type=str, help="Name of function to test")
    parser.add_argument(
        "--apikey", type=str, help="OpenAI API key for integration tests"
    )
    args = parser.parse_args()

    if args.directory:
        os.environ["TEST_DIRECTORY"] = args.directory
    if args.apikey:
        os.environ["OPENAI_KEY"] = args.apikey

    # pytest.main(["-x", "-s", "sageai/tests/unit.py"])
    pytest.main(["-x", "-s", "sageai/tests/integration.py"])
