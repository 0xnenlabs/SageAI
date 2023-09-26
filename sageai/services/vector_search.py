import openai
import faiss

from sageai.config import get_config
from sageai.services.openai import OpenAIService


class VectorSearchService:
    def __init__(self):
        self.data = []
        self.dim = 768
        self.index = faiss.IndexFlatL2(self.dim)
        self.openai_service = OpenAIService()

        openai.api_key = get_config().openai_key

    def index_data(self, new_data: str):
        new_vectors = self.openai_service.create_embeddings(new_data)
        if new_vectors:
            self.data.extend(new_data)
            self.index.add(new_vectors)

    def search(self, query: str, k: int = 5):
        if query_vector is None:
            return []

        query_vector = self.openai_service.create_embeddings(query)
        _, I = self.index.search(query_vector, k)
        return [self.data[i] for i in I[0]]
