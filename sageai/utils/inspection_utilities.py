import inspect
from typing import Callable, Type

from pydantic import BaseModel


def get_input_parameter_type(function: Callable) -> Type[BaseModel]:
    signature = inspect.signature(function)
    for name, param in signature.parameters.items():
        if "Input" in str(param.annotation):
            return param.annotation
    raise Exception(f"Could not find Input parameter type from function arguments.")
