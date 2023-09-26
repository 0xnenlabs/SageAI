import openai
import numpy as np
import faiss
import time

from sageai.config import get_config


class VectorDBService:
    def __init__(self):
        self.data = []
        self.dim = 768
        self.index = faiss.IndexFlatL2(self.dim)

        openai.api_key = get_config().openai_key

    def index_data(self, new_data):
        new_vectors = self._data_to_vector(new_data)
        if new_vectors:
            self.data.extend(new_data)
            self.index.add(new_vectors)

    def search(self, query, k=5):
        query_vector = self._query_to_vector(query)
        if query_vector is not None:
            D, I = self.index.search(query_vector, k)
            return [self.data[i] for i in I[0]]
        else:
            return []

    def _data_to_vector(self, data):
        try:
            response = openai.Embed.create(model="gpt-3.5-turbo", texts=data)
            embeddings = np.array([entry["embedding"] for entry in response["data"]])
            time.sleep(1)
            return embeddings
        except openai.error.OpenaiError as e:
            print(f"Error encountered: {e}")
            return []

    def _query_to_vector(self, query):
        try:
            response = openai.Embed.create(model="gpt-3.5-turbo", texts=[query])
            embedding = np.array(response["data"][0]["embedding"]).reshape(1, -1)
            return embedding
        except openai.error.OpenaiError as e:
            print(f"Error encountered: {e}")
            return None
