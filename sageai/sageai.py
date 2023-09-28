import json
from typing import Any, Dict, Optional, Type

from sageai.config import LogLevel, get_config, get_function_map, set_config
from sageai.services.openai_service import OpenAIService
from sageai.types.abstract_vectordb import AbstractVectorDB
from sageai.utils.inspection_utilities import get_input_parameter_type
from sageai.utils.openai_utilities import get_latest_user_message


class SageAI:
    def __init__(
        self,
        *,
        openai_key: str,
        functions_directory: Optional[str] = None,
        vectordb: Optional[Type[AbstractVectorDB]] = None,
        log_level: Optional[LogLevel] = None,
    ):
        if openai_key is None:
            raise Exception("No OpenAI key provided.")

        config_args = {"openai_key": openai_key}

        if functions_directory is not None:
            config_args["functions_directory"] = functions_directory
        if vectordb is not None:
            config_args["vectordb"] = vectordb
        if log_level is not None:
            config_args["log_level"] = LogLevel(log_level)

        set_config(**config_args)
        self.config = get_config()

        self.openai = OpenAIService()
        self.vectordb = self.config.vectordb()

    def chat(self, *args, **kwargs) -> str:
        merged = {i: v for i, v in enumerate(args)}
        merged.update(kwargs)

        top_n = merged.pop("top_n") if "top_n" in merged else None

        if merged.get("model") is None:
            raise Exception("No model provided.")

        if merged.get("messages") is None:
            raise Exception("No messages provided.")

        if top_n is None:
            raise Exception("No top_n provided.")

        latest_user_message = get_latest_user_message(merged.get("messages"))
        if latest_user_message is None:
            raise Exception("No user message found.")

        top_functions = self.get_top_n_functions(
            query=latest_user_message["content"], top_n=top_n
        )

        openai_result = self.openai.chat(**merged, functions=top_functions)

        if "function_call" not in openai_result:
            raise Exception("No function call found in OpenAI response.")

        function_name = openai_result["function_call"]["name"]
        function_args = json.loads(openai_result["function_call"]["arguments"])
        function_response = self.run_function(name=function_name, args=function_args)
        return function_response, function_name, function_args
        # return {
        #     "result": function_response,
        #     "vectordb_result": top_functions,
        #     "openai_function_name": function_name,
        #     "openai_function_args": function_args,
        # }

    def get_top_n_functions(self, *, query: str, top_n: int):
        return self.vectordb.search_impl(query=query, top_n=top_n)

    @staticmethod
    def run_function(*, name: str, args: Dict[str, Any]):
        function_map = get_function_map()
        func = function_map[name]
        function_input_type = get_input_parameter_type(func.function)
        func_args = function_input_type(**args)
        func_result = func(func_args)
        return func_result.dict()

    def index(self):
        self.vectordb.index()
