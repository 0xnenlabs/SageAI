import argparse
import os

import pytest


def main():
    parser = argparse.ArgumentParser(description="Run tests for functions.")
    parser.add_argument("--directory", type=str, help="Name of function to test")
    parser.add_argument(
        "--apikey", type=str, help="OpenAI API key for integration tests"
    )
    parser.add_argument("--unit", action="store_true", help="Run only the unit tests")
    parser.add_argument(
        "--integration", action="store_true", help="Run only the integration tests"
    )
    args = parser.parse_args()

    if args.directory:
        os.environ["TEST_DIRECTORY"] = args.directory
    if args.apikey:
        os.environ["OPENAI_KEY"] = args.apikey

    current_directory = os.path.dirname(os.path.abspath(__file__))

    if not args.integration or args.unit:
        unit_test_path = os.path.join(current_directory, "unit.py")
        pytest.main(["-x", "-s", unit_test_path, "--disable-warnings"])
    if not args.unit or args.integration:
        integration_test_path = os.path.join(current_directory, "integration.py")
        pytest.main(["-x", "-s", integration_test_path, "--disable-warnings"])
