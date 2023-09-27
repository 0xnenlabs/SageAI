from typing import Any, List, Dict

import openai


class OpenAIService:
    def __init__(self):
        from sageai.config import get_config

        config = get_config()
        openai.api_key = config.openai_key
        self.openai = openai

    def create_embeddings(self, *args, **kwargs) -> List[float]:
        response = self.openai.Embedding.create(*args, **kwargs)
        embeddings = response["data"][0]["embedding"]
        return embeddings

    def chat(self, *args, **kwargs) -> Dict[str, Any]:
        response = self.openai.ChatCompletion.create(*args, **kwargs)
        response_message = response["choices"][0]["message"]
        return response_message

    @staticmethod
    def get_embeddings_size():
        return 1536
