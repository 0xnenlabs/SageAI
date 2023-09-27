from typing import List, Dict, Any

from sageai import SageAI
from sageai.types.function import Function
from sageai.types.abstract_vectordb import AbstractVectorDB


# Define your own VectorDB implementation:
class CustomVectorDBService(AbstractVectorDB):
    def __init__(self, function_map: dict[str, Function]):
        super().__init__(function_map=function_map)
        self.function_map = function_map
        # ...other initialisation logic

    # function to index the function map to your vectorDB
    def index(self):
        self.indexed = self.function_map

    # create and return embeddings for query
    def embed(self, query: str):
        embeddings = query
        return embeddings

    # Any pre-processing you want to apply to the query (e.g. lowercasing)
    def format_query(self, *, query: str):
        return query.lower()

    def search(self, query: str, k: int) -> List[Dict[str, Any]]:
        formatted_query = self.format_query(query=query)
        query_embedding = self.embed(query=formatted_query)

        # Search VectorDB and retreive function names
        func_names = ["get_current_weather", "other_function_name"]

        return self.format_search_result(function_names=func_names)


# Init on startup
sageai = SageAI(
    openai_key="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",
    functions_directory="functions",
    log_level="WARNING",
    vectordb=CustomVectorDBService,
)

# In a CI/CD pipeline or in dev mode on startup/hot reload
sageai.index()

# Anywhere in the codebase
message = "What's the weather like in Boston right now?"
response = sageai.chat(message=message)

print(message)
print(response)
