from abc import ABC, abstractmethod
from typing import List

from sageai.types.function import Function


class AbstractVectorDB(ABC):
    def __init__(self, function_map: dict[str, Function]):
        pass

    @abstractmethod
    def index(self) -> None:
        """Indexes the vector db based on the functions directory."""
        pass

    def embed(self, *, query: str):
        """Embeds a query."""
        pass

    def format_query(self, *, query: str) -> str:
        """Formats a query for embedding."""
        pass

    @abstractmethod
    def search(self, *, query: str, n: int) -> List[str]:
        """Search vector db based on a query and return top n function names."""
        pass
