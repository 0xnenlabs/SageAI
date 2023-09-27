import json
from typing import Optional, Dict, Any

from sageai.config import get_config, set_config
from sageai.services.defaultvectordb_service import DefaultVectorDBService
from sageai.services.openai_service import OpenAIService
from sageai.types.function import Function
from sageai.utils import generate_functions_map
from sageai.utils.inspection_utilities import get_input_parameter_type


class SageAI:
    def __init__(
        self,
        *,
        openai_key: str,
        functions_directory: Optional[str] = None,
        function_calling_model: Optional[str] = None,
        embeddings_model: Optional[str] = None,
        vectordb: Optional = None,
    ):
        config_args = {
            "openai_key": openai_key
        }

        if functions_directory is not None:
            config_args["functions_directory"] = functions_directory
        if function_calling_model is not None:
            config_args["function_calling_model"] = function_calling_model
        if embeddings_model is not None:
            config_args["embeddings_model"] = embeddings_model
        set_config(**config_args)
        self.config = get_config()
        self.function_map: Dict[str, Function] = generate_functions_map(
            self.config.functions_directory
        )
        self.vectordb = vectordb or DefaultVectorDBService()
        self.openai = OpenAIService()

    def chat(self, *, message: str, options: Optional[Dict] = None) -> str:
        """
        High-level function that calls the vector database, OpenAI, and the function, and returns
        the result.
        :param message: the message
        :param options:
        :return:
        """
        if options is None:
            options = {}

        top_functions = self.get_top_n_functions(message=message, k=options.get("k") or 5)
        openai_result = self.openai.chat(
            functions=top_functions,
            message=message,
        )

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
