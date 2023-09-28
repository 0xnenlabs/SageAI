from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AbstractVectorDB(ABC):
    def __init__(self):
        from sageai.config import get_function_map

        self.function_map = get_function_map()

    @abstractmethod
    def index(self) -> None:
        """Indexes the vector db based on the functions directory."""
        pass

    @abstractmethod
    def search(self, *, query: str, top_n: int) -> List[str]:
        """Actual search logic, which should be implemented in derived classes.
        It should return a list of function names
        """
        pass

    def format_search_result(
        self, *, function_names: List[str]
    ) -> List[Dict[str, Any]]:
        potential_functions = [
            self.function_map[func_name].parameters for func_name in function_names
        ]
        return potential_functions

    def search_impl(self, *, query: str, top_n: int) -> List[Dict[str, Any]]:
        """Search vector db based on a query and return top n function names."""
        results = self.search(query=query, top_n=top_n)
        return self.format_search_result(function_names=results)
