from typing import Optional, Dict

from sageai.config import get_config, set_config
from sageai.services.defaultvectordb_service import DefaultVectorDBService
from sageai.services.openai_service import OpenAIService
from sageai.types.function import Function
from sageai.utils import generate_functions_map


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
            messages=[message],
        )
        print("response: ", openai_result)
        return openai_result

    def get_top_n_functions(self, *, message: str, k: int):
        return self.vectordb.search(query=message, k=k)

    def run_function(self, *, message: str):
        return message

    # @staticmethod
    # def run_message(message: str, model: Optional[str] = "gpt-3.5-turbo-0613") -> Any:
    #     pass

    #     # # Vector DB Search
    #     # vector_search_start_time = time.time()
    #     # potential_function_names = self.db.get_top_n(message=message)
    #     # potential_functions = [
    #     #     self.func_map[func_name].parameters
    #     #     for func_name in potential_function_names
    #     # ]
    #     # vector_search_end_time = time.time()
    #     # vector_search_processing_time = round(
    #     #     vector_search_end_time - vector_search_start_time,
    #     #     1,
    #     # )

    #     # # OpenAI Functions
    #     # idx = 0
    #     # while idx < self.MAX_FUNC_CALLS:
    #     #     try:
    #     #         openai_start_time = time.time()
    #     #         self.logger.info(f"Running chat on loop {idx}...")
    #     #         chat = services.openai.get_chat(
    #     #             model=model,
    #     #             temperature=0,
    #     #             functions=potential_functions,
    #     #         )
    #     #         response = chat(self.message_history)

    #     #         openai_end_time = time.time()
    #     #         openai_processing_time = round(openai_end_time - openai_start_time, 1)
    #     #         # if model doesn't choose a function
    #     #         if not response.additional_kwargs:
    #     #             function_return = FunctionReturnType(
    #     #                 data=NoFunctionChosenData(display_content=response.content),
    #     #                 error="NO_FUNCTION_CHOSEN",
    #     #             )
    #     #             total_processing_time = (
    #     #                 vector_search_processing_time + openai_processing_time
    #     #             )
    #     #             result = SenninReturnType(
    #     #                 potential_functions=potential_function_names,
    #     #                 function=None,
    #     #                 parameters=None,
    #     #                 result=function_return,
    #     #                 suggestions=None,
    #     #                 processing_times=ProcessingTimes(
    #     #                     vector_search=vector_search_processing_time,
    #     #                     openai=openai_processing_time,
    #     #                     function=None,
    #     #                     total=total_processing_time,
    #     #                 ),
    #     #             )
    #     #             self.result_history.append(result)
    #     #             break

    #     #         function_call = response.additional_kwargs["function_call"]
    #     #         function_call_start_time = time.time()
    #     #         self.logger.info(f"OpenAI Function call: {function_call}")
    #     #         function_name = function_call["name"]
    #     #         function_to_call = self.func_map[function_name]
    #     #         model_function_args = json.loads(function_call["arguments"])
    #     #         self.logger.info(f"Model function args: {model_function_args}")
    #     #         function_args = replace_keywords_in_args(
    #     #             args=model_function_args,
    #     #             keyword_map=keyword_map,
    #     #         )
    #     #         self.logger.info(f"Function args: {function_args}")

    #     #         function_input_type = get_input_parameter_type(
    #     #             function_to_call.function,
    #     #         )
    #     #         self.logger.info(f"Function input type: {function_input_type}")

    #     #         function_parameters = function_input_type(**function_args)
    #     #         function_response: FunctionReturnType = function_to_call(
    #     #             function_parameters,
    #     #             logger=self.logger,
    #     #         )

    #     #         function_call_end_time = time.time()
    #     #         function_call_processing_time = round(
    #     #             function_call_end_time - function_call_start_time,
    #     #             1,
    #     #         )

    #     #         total_processing_time = (
    #     #             vector_search_processing_time
    #     #             + openai_processing_time
    #     #             + function_call_processing_time
    #     #         )
    #     #         processing_times = ProcessingTimes(
    #     #             vector_search=vector_search_processing_time,
    #     #             openai=openai_processing_time,
    #     #             function=function_call_processing_time,
    #     #             total=total_processing_time,
    #     #         )

    #     #         filtered_function_names = list(
    #     #             filter(lambda x: x != function_name, potential_function_names),
    #     #         )
    #     #         suggestions = filtered_function_names[0 : self.MAX_SUGGESTIONS]

    #     #         result = SenninReturnType(
    #     #             potential_functions=potential_function_names,
    #     #             function=function_to_call,
    #     #             parameters=function_parameters,
    #     #             result=function_response,
    #     #             suggestions=suggestions,
    #     #             processing_times=processing_times.dict(),
    #     #         )
    #     #         self.result_history.append(result)
    #     #     except Exception as e:
    #     #         self.logger.exception(f"Error running function: {e}")
    #     #         break
    #     #     finally:
    #     #         idx += 1

    #     # return self.result_history

    # @staticmethod
    # def run_function(func_name: str, args: Optional[dict[str, Any]] = None) -> Any:
    #     pass
    #     # self.logger.info(
    #     #     f"\n[Sennin] Running function: {func_name} with args {args}, keyword map {keyword_map}",
    #     # )
    #     # if func_name not in self.func_map:
    #     #     raise Exception(f"Function {func_name} not found.")
    #     # function_to_call = self.func_map[func_name]
    #     # formatted_args = replace_keywords_in_args(args=args, keyword_map=keyword_map)
    #     # function_input = function_to_call.input_type(
    #     #     **formatted_args if formatted_args is not None else {}
    #     # )
    #     # function_call_start_time = time.time()
    #     # function_response = function_to_call(function_input, logger=self.logger)
    #     # function_call_end_time = time.time()
    #     # function_call_processing_time = round(
    #     #     function_call_end_time - function_call_start_time,
    #     #     1,
    #     # )

    #     # processing_times = {
    #     #     "vector_search": None,
    #     #     "openai": None,
    #     #     "function": function_call_processing_time,
    #     #     "total": function_call_processing_time,
    #     # }

    #     # formatted_embedding = self.db.format_func_embedding(function_to_call)
    #     # similar_func_names = self.db.get_top_n(
    #     #     message=formatted_embedding,
    #     #     n=self.MAX_SUGGESTIONS + 1,
    #     # )
    #     # filtered_function_names = list(
    #     #     filter(lambda x: x != func_name, similar_func_names),
    #     # )
    #     # suggestions = filtered_function_names[0 : self.MAX_SUGGESTIONS]

    #     # return SenninReturnType(
    #     #     potential_functions=None,
    #     #     function=function_to_call,
    #     #     parameters=function_input,
    #     #     result=function_response,
    #     #     suggestions=suggestions,
    #     #     processing_times=processing_times,
    #     # )
