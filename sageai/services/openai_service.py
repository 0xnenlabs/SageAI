from typing import Any, Dict, List, Literal, Optional, Union

from openai import OpenAI
from openai._types import NOT_GIVEN


class OpenAIService:
    def __init__(self):
        from sageai.config import get_config

        config = get_config()

        self.client = OpenAI(api_key=config.openai_key)

    def create_embeddings(
        self,
        *,
        input: Union[str, List[str], List[int], List[List[int]]],
        model: Union[str, Literal["text-embedding-ada-002"]],
        encoding_format: Optional[Literal["float", "base64"]] = NOT_GIVEN,
        user: Optional[str] = NOT_GIVEN,
        **kwargs,
    ) -> List[float]:
        response = self.client.embeddings.create(
            input=input,
            model=model,
            encoding_format=encoding_format,
            user=user,
            **kwargs,
        )
        embeddings = response.data[0].embedding
        return embeddings

    def chat(
        self,
        *,
        messages: List[Dict[str, str]],
        model: str,
        function_call: Optional[Dict[str, Any]] = NOT_GIVEN,
        functions: Dict[str, Any] = NOT_GIVEN,
        max_tokens: Optional[int] = NOT_GIVEN,
        response_format: Optional[Literal["string", "json"]] = NOT_GIVEN,
        temperature: Optional[float] = NOT_GIVEN,
        **kwargs,
    ) -> Dict[str, Any]:
        response = self.client.chat.completions.create(
            messages=messages,
            model=model,
            function_call=function_call,
            functions=functions,
            max_tokens=max_tokens,
            response_format=response_format,
            temperature=temperature,
            **kwargs,
        )
        response_message = response.choices[0].message
        return response_message

    @staticmethod
    def get_embeddings_size():
        return 1536
