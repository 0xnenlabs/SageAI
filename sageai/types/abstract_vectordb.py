from abc import ABC, abstractmethod
from typing import List

from sageai.types.function import Function


class AbstractVectorDB(ABC):
    def __init__(self, function_map: dict[str, Function]):
        self.function_map = function_map

    def format_search_result(self, function_names: List[str]):
        potential_functions = [
            self.function_map[func_name].parameters for func_name in function_names
        ]
        return potential_functions

    @abstractmethod
    def index(self) -> None:
        """Indexes the vector db based on the functions directory."""
        pass

    @abstractmethod
    def embed(self, *, query: str):
        """Embeds a query."""
        pass

    @abstractmethod
    def format_query(self, *, query: str) -> str:
        """Formats a query for embedding."""
        pass

    @abstractmethod
    def search(self, *, query: str, n: int) -> List[str]:
        """Search vector db based on a query and return top n function names."""
        pass
