from typing import Any, Dict, List

from qdrant_client import QdrantClient
from qdrant_client.http.models import models

from sageai.services.openai_service import OpenAIService
from sageai.types.abstract_vectordb import AbstractVectorDB
from sageai.types.function import Function


class DefaultVectorDBService(AbstractVectorDB):
    def __init__(self, function_map: dict[str, Function]):
        self.client = QdrantClient(":memory:")
        self.openai = OpenAIService()
        self.collection = "functions"
        self.function_map = function_map

    def index(self):
        self.client.recreate_collection(
            collection_name=self.collection,
            vectors_config=models.VectorParams(
                size=self.openai.get_embeddings_size(),
                distance=models.Distance.COSINE,
            ),
        )

        def format_func_embedding(func: Function) -> str:
            embedding_text = func.name.replace("_", " ") + " - " + func.description
            return self.format_query(query=embedding_text)

        records = [
            models.Record(
                id=idx,
                vector=self.openai.create_embeddings(text=format_func_embedding(func)),
                payload={"func_name": func_name},
            )
            for idx, (func_name, func) in enumerate(self.function_map.items())
        ]
        self.client.upload_records(
            collection_name=self.collection,
            records=records,
        )

    def embed(self, query: str):
        return self.openai.create_embeddings(query)

    def format_query(self, *, query: str):
        return query.lower()

    def search(self, query: str, k: int) -> List[Dict[str, Any]]:
        formatted_query = self.format_query(query=query)
        query_embedding = self.openai.create_embeddings(text=formatted_query)
        hits = self.client.search(
            collection_name=self.collection,
            query_vector=query_embedding,
            limit=k,
        )
        func_names = [hit.payload["func_name"] for hit in hits]
        potential_functions = [
            self.function_map[func_name].parameters for func_name in func_names
        ]
        return potential_functions
