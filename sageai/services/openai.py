from typing import Any, List
from logging import getLogger
import numpy as np

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

    def create_embeddings(self, text: str):
        response = self.openai.Embedding.create(
            input=text,
            model=self.embeddings_model,
        )
        embeddings = np.array([entry["embedding"] for entry in response["data"]])
        return embeddings

    def chat(
        self, functions: List[dict[str, Any]], messages, model: str, temperature: float
    ):
        response = openai.ChatCompletion.create(
            model=model if model else self.function_calling_model,
            temperature=temperature if temperature else None,
            messages=messages,
            functions=functions,
            function_call="auto",
        )
        response_message = response["choices"][0]["message"]
        return response_message
