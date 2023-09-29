from typing import List

from vectordb import Memory

from sageai.types.abstract_vectordb import AbstractVectorDB


class CustomVectorDB(AbstractVectorDB):
    def __init__(self):
        super().__init__()
        self.memory = Memory()

    def index(self):
        self.memory.clear()
        for func_name, func in self.function_map.items():
            self.memory.save(func_name, func)

    def search(self, query: str, n: int) -> List[str]:
        return self.memory.search(query, top_n=n)
