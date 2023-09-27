from typing import Any, Dict, List

from qdrant_client import QdrantClient
from qdrant_client.http.models import models

from sageai.services.openai_service import OpenAIService
from sageai.types.abstract_vectordb import AbstractVectorDB
from sageai.types.function import Function


class CustomVectorDB(AbstractVectorDB):
    def __init__(self):
        super().__init__()

        self.openai = OpenAIService()
        self.client = QdrantClient(":memory:")
        self.collection = "functions"

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
                vector=self.openai.create_embeddings(
                    model="text-embedding-ada-002", input=format_func_embedding(func)
                ),
                payload={"func_name": func_name},
            )
            for idx, (func_name, func) in enumerate(self.function_map.items())
        ]
        self.client.upload_records(
            collection_name=self.collection,
            records=records,
        )

    def embed(self, query: str):
        return self.openai.create_embeddings(
            model="text-embedding-ada-002",
            input=query,
        )

    def format_query(self, *, query: str):
        return query.lower()

    def search(self, query: str, k: int) -> List[Dict[str, Any]]:
        formatted_query = self.format_query(query=query)
        query_embedding = self.embed(query=formatted_query)
        hits = self.client.search(
            collection_name=self.collection,
            query_vector=query_embedding,
            limit=k,
        )
        func_names = [hit.payload["func_name"] for hit in hits]

        return self.format_search_result(function_names=func_names)
