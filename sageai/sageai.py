import json
from typing import Optional, Dict, Any

from sageai.config import get_config, set_config, LogLevel
from sageai.services.openai_service import OpenAIService
from sageai.types.abstract_vectordb import AbstractVectorDB
from sageai.utils.generate_functions_map import generate_functions_map
from sageai.utils.inspection_utilities import get_input_parameter_type
from sageai.utils.openai_utilities import get_latest_user_message


class SageAI:
    def __init__(
        self,
        *,
        openai_key: str,
        functions_directory: Optional[str] = None,
        vectordb: Optional[AbstractVectorDB] = None,
        log_level: Optional[LogLevel] = None,
    ):
        config_args = {"openai_key": openai_key}

        if functions_directory is not None:
            config_args["functions_directory"] = functions_directory
        if log_level is not None:
            config_args["log_level"] = LogLevel(log_level)
        if vectordb is not None:
            config_args["vectordb"] = vectordb

        set_config(**config_args)
        self.config = get_config()

        self.openai = OpenAIService()
        self.function_map = generate_functions_map(self.config.functions_directory)
        self.vectordb = self.config.vectordb(function_map=self.function_map)

    def chat(self, *args, **kwargs) -> str:
        merged = {i: v for i, v in enumerate(args)}
        merged.update(kwargs)

        sageai_dict = {key: merged[key] for key in ["sageai"] if key in merged}
        sageai_dict = sageai_dict["sageai"] if "sageai" in sageai_dict else {}
        openai_dict = {key: merged[key] for key in merged if key != "sageai"}

        if openai_dict.get("model") is None:
            raise Exception("No model provided.")

        if openai_dict.get("messages") is None:
            raise Exception("No messages provided.")

        if sageai_dict.get("k") is None:
            raise Exception("No k provided.")

        latest_user_message = get_latest_user_message(openai_dict.get("messages"))
        if latest_user_message is None:
            raise Exception("No user message found.")

        top_functions = self.get_top_n_functions(
            message=latest_user_message["content"], k=sageai_dict.get("k")
        )
        openai_result = self.openai.chat(**openai_dict, functions=top_functions)

        if "function_call" not in openai_result:
            raise Exception("No function call found in OpenAI response.")

        function_to_call = openai_result["function_call"]["name"]
        function_args = json.loads(openai_result["function_call"]["arguments"])
        function_response = self.run_function(
            name=function_to_call,
            args=function_args,
        )
        return function_response

    def get_top_n_functions(self, *, message: str, k: int):
        return self.vectordb.search(query=message, k=k)

    def run_function(self, *, name: str, args: Dict[str, Any]):
        func = self.function_map[name]
        function_input_type = get_input_parameter_type(func.function)
        func_args = function_input_type(**args)
        return func(func_args)

    def index(self):
        self.vectordb.index()
