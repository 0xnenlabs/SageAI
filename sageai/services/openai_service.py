from logging import getLogger
from typing import Any, List, Dict

import openai

from sageai.config import get_config


class OpenAIService:
    def __init__(self):
        self.logger = getLogger(__name__)

        config = get_config()
        self.api_key = config.openai_key
        self.function_calling_model = config.function_calling_model
        self.embeddings_model = config.embeddings_model

        openai.api_key = self.api_key
        self.openai = openai

    def create_embeddings(self, text: str) -> List[float]:
        response = self.openai.Embedding.create(
            input=text,
            model=self.embeddings_model,
        )
        embeddings = response["data"][0]["embedding"]
        return embeddings

    def chat(
        self,
        functions: List[dict[str, Any]],
        message: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        response = openai.ChatCompletion.create(
            model=kwargs["model"] if "model" in kwargs else self.function_calling_model,
            messages=[dict(role="user", content=message)],
            functions=functions,
            **kwargs,
        )
        response_message = response["choices"][0]["message"]
        return response_message

    @staticmethod
    def get_embeddings_size():
        return 1536
