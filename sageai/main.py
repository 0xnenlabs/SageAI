from typing import Any, Optional

from sageai.config import get_config

# import openai


class SageAI:
    MAX_SUGGESTIONS = 3
    MAX_FUNC_CALLS = 1

    def ask(self, message: str):
        print("MESSAGE: ", message)

        config = get_config()
        print("CONFIG: ", config)

        functions_path = config.functions_path
        with open(functions_path, "r") as file:
            content = file.read()

        return content

    def run_message(
        self, message: str, model: Optional[str] = "gpt-3.5-turbo-0613"
    ) -> Any:
        pass
        # self.reset()

        # self.logger.info(f"Running message: {message}")
        # # TODO when this turns into an actual application with memory and history,
        # #  this should be switched to a session-based set not a reset.
        # #  this means get the user's message and result history and set it properly on the instance.
        # self.message_history.append(SystemMessage(content=get_system_prompt()))
        # self.message_history.append(HumanMessage(content=message))

        # # Vector DB Search
        # vector_search_start_time = time.time()
        # potential_function_names = self.db.get_top_n(message=message)
        # potential_functions = [
        #     self.func_map[func_name].parameters
        #     for func_name in potential_function_names
        # ]
        # vector_search_end_time = time.time()
        # vector_search_processing_time = round(
        #     vector_search_end_time - vector_search_start_time,
        #     1,
        # )

        # # OpenAI Functions
        # idx = 0
        # while idx < self.MAX_FUNC_CALLS:
        #     try:
        #         openai_start_time = time.time()
        #         self.logger.info(f"Running chat on loop {idx}...")
        #         chat = services.openai.get_chat(
        #             model=model,
        #             temperature=0,
        #             functions=potential_functions,
        #         )
        #         response = chat(self.message_history)

        #         openai_end_time = time.time()
        #         openai_processing_time = round(openai_end_time - openai_start_time, 1)
        #         # if model doesn't choose a function
        #         if not response.additional_kwargs:
        #             function_return = FunctionReturnType(
        #                 data=NoFunctionChosenData(display_content=response.content),
        #                 error="NO_FUNCTION_CHOSEN",
        #             )
        #             total_processing_time = (
        #                 vector_search_processing_time + openai_processing_time
        #             )
        #             result = SenninReturnType(
        #                 potential_functions=potential_function_names,
        #                 function=None,
        #                 parameters=None,
        #                 result=function_return,
        #                 suggestions=None,
        #                 processing_times=ProcessingTimes(
        #                     vector_search=vector_search_processing_time,
        #                     openai=openai_processing_time,
        #                     function=None,
        #                     total=total_processing_time,
        #                 ),
        #             )
        #             self.result_history.append(result)
        #             break

        #         function_call = response.additional_kwargs["function_call"]
        #         function_call_start_time = time.time()
        #         self.logger.info(f"OpenAI Function call: {function_call}")
        #         function_name = function_call["name"]
        #         function_to_call = self.func_map[function_name]
        #         model_function_args = json.loads(function_call["arguments"])
        #         self.logger.info(f"Model function args: {model_function_args}")
        #         function_args = replace_keywords_in_args(
        #             args=model_function_args,
        #             keyword_map=keyword_map,
        #         )
        #         self.logger.info(f"Function args: {function_args}")

        #         function_input_type = get_input_parameter_type(
        #             function_to_call.function,
        #         )
        #         self.logger.info(f"Function input type: {function_input_type}")

        #         function_parameters = function_input_type(**function_args)
        #         function_response: FunctionReturnType = function_to_call(
        #             function_parameters,
        #             logger=self.logger,
        #         )

        #         function_call_end_time = time.time()
        #         function_call_processing_time = round(
        #             function_call_end_time - function_call_start_time,
        #             1,
        #         )

        #         total_processing_time = (
        #             vector_search_processing_time
        #             + openai_processing_time
        #             + function_call_processing_time
        #         )
        #         processing_times = ProcessingTimes(
        #             vector_search=vector_search_processing_time,
        #             openai=openai_processing_time,
        #             function=function_call_processing_time,
        #             total=total_processing_time,
        #         )

        #         filtered_function_names = list(
        #             filter(lambda x: x != function_name, potential_function_names),
        #         )
        #         suggestions = filtered_function_names[0 : self.MAX_SUGGESTIONS]

        #         result = SenninReturnType(
        #             potential_functions=potential_function_names,
        #             function=function_to_call,
        #             parameters=function_parameters,
        #             result=function_response,
        #             suggestions=suggestions,
        #             processing_times=processing_times.dict(),
        #         )
        #         self.result_history.append(result)
        #     except Exception as e:
        #         self.logger.exception(f"Error running function: {e}")
        #         break
        #     finally:
        #         idx += 1

        # return self.result_history

    def run_function(
        self, func_name: str, args: Optional[dict[str, Any]] = None
    ) -> Any:
        pass
        # self.logger.info(
        #     f"\n[Sennin] Running function: {func_name} with args {args}, keyword map {keyword_map}",
        # )
        # if func_name not in self.func_map:
        #     raise Exception(f"Function {func_name} not found.")
        # function_to_call = self.func_map[func_name]
        # formatted_args = replace_keywords_in_args(args=args, keyword_map=keyword_map)
        # function_input = function_to_call.input_type(
        #     **formatted_args if formatted_args is not None else {}
        # )
        # function_call_start_time = time.time()
        # function_response = function_to_call(function_input, logger=self.logger)
        # function_call_end_time = time.time()
        # function_call_processing_time = round(
        #     function_call_end_time - function_call_start_time,
        #     1,
        # )

        # processing_times = {
        #     "vector_search": None,
        #     "openai": None,
        #     "function": function_call_processing_time,
        #     "total": function_call_processing_time,
        # }

        # formatted_embedding = self.db.format_func_embedding(function_to_call)
        # similar_func_names = self.db.get_top_n(
        #     message=formatted_embedding,
        #     n=self.MAX_SUGGESTIONS + 1,
        # )
        # filtered_function_names = list(
        #     filter(lambda x: x != func_name, similar_func_names),
        # )
        # suggestions = filtered_function_names[0 : self.MAX_SUGGESTIONS]

        # return SenninReturnType(
        #     potential_functions=None,
        #     function=function_to_call,
        #     parameters=function_input,
        #     result=function_response,
        #     suggestions=suggestions,
        #     processing_times=processing_times,
        # )
