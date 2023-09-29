from typing import Any, Callable, Dict, List, Type

from pydantic import BaseModel

from sageai.utils.inspection_utilities import get_input_parameter_type
from sageai.utils.model_utilities import (
    get_array_item_type,
    get_enum_array_values,
    get_possible_values,
    is_array,
    is_enum,
    is_enum_array,
    is_optional,
)


class Function(BaseModel):
    # required
    function: Callable
    description: str

    # generated from input
    name: str
    parameters: Dict[str, Any]
    input_type: Type[BaseModel]

    def __init__(
        self,
        function: Callable,
        description: str,
    ) -> None:
        name = function.__name__
        input_parameter_type = get_input_parameter_type(function)
        formatted_parameters = self._format_parameters(
            input_parameter_type=input_parameter_type,
            name=name,
            description=description,
        )

        super().__init__(
            function=function,
            description=description,
            name=name,
            parameters=formatted_parameters,
            input_type=input_parameter_type,
        )

    @staticmethod
    def _format_parameters(input_parameter_type, name: str, description: str):
        parameters = input_parameter_type.schema()
        new_schema = {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }

        for key, value in parameters["properties"].items():
            if is_enum_array(input_parameter_type, key):
                enum_values = get_enum_array_values(input_parameter_type, key)
                enum_type = "integer" if isinstance(enum_values[0], int) else "string"
                property_schema = {
                    "type": "array",
                    "description": value.get("description", ""),
                    "items": {"type": enum_type, "enum": enum_values},
                }
            elif is_enum(input_parameter_type, key):
                property_schema = {
                    "type": "string",
                    "description": value["description"],
                    "enum": get_possible_values(input_parameter_type, key),
                }
            elif is_array(input_parameter_type, key):
                property_schema = {
                    "type": "array",
                    "description": value.get("description", ""),
                    "items": {
                        "type": get_array_item_type(input_parameter_type, key),
                    },
                }
            else:
                property_type = value.get("type")
                if property_type is None:
                    raise Exception("Property type is None")
                property_schema = {
                    "type": property_type,
                    "description": value.get("description", ""),
                }

            new_schema["parameters"]["properties"][key] = property_schema

            # Check if the property is required
            if not is_optional(input_parameter_type, key):
                new_schema["parameters"]["required"].append(key)

        return new_schema

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def __str__(self):
        return f"{self.name}: {self.description}"
