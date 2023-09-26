import inspect
from typing import Any, Callable, Dict, List, Type
from pydantic import BaseModel


def get_input_parameter_types(function: Callable) -> List[Type[BaseModel]]:
    signature = inspect.signature(function)
    param_types = [param.annotation for _, param in signature.parameters.items()]

    return param_types


class Function(BaseModel):
    # required
    function: Callable
    description: str

    # generated from input
    name: str
    parameters: Dict[str, Any]
    input_types: List[Type[BaseModel]]

    def __init__(
        self,
        function: Callable,
        description: str,
    ) -> None:
        name = function.__name__
        input_parameter_types = get_input_parameter_types(function)

        super().__init__(
            function=function,
            description=description,
            name=name,
            input_types=input_parameter_types,
        )

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.model_description}"
