from enum import Enum
from types import ModuleType
from typing import Any, List, Optional, Type, Union, get_args, get_origin

from pydantic import BaseModel


def find_pydantic_model(
    module: ModuleType,
    keyword: str,
) -> Type[BaseModel] | None:
    models = [
        cls
        for name, cls in vars(module).items()
        if isinstance(cls, type)
        and issubclass(cls, BaseModel)
        and name.endswith(
            keyword,
        )
    ]
    return models[0] if models else None


def get_input_model(module: ModuleType) -> Type[BaseModel]:
    return find_pydantic_model(module, keyword="Input")


def get_output_data_model(module: ModuleType) -> Type[BaseModel]:
    return find_pydantic_model(module, keyword="Data")


def is_enum(model: Type[BaseModel], key: str) -> bool:
    if key in model.__annotations__:
        annotation = model.__annotations__[key]
        # Check if annotation is a class
        if isinstance(annotation, type):
            return issubclass(annotation, Enum)
        # Handle Optional[Enum] and List[Enum]
        origin = get_origin(annotation)
        if origin in {Optional, List, Union}:
            args = get_args(annotation)
            if args and isinstance(args[0], type):
                return issubclass(args[0], Enum)
    return False


def get_possible_values(model: Type[BaseModel], key: str) -> List[str] | List[int]:
    if is_enum(model, key) or is_enum_array(model, key):
        enum_type = model.__annotations__[key]
        if get_origin(enum_type) in {Optional, Union, List}:
            enum_type = get_args(enum_type)[0]
        return [e.value for e in enum_type]
    return []


def is_optional(model: Type[BaseModel], key: str) -> bool:
    annotation = model.__annotations__[key]
    return type(None) in get_args(annotation)


def is_array(model: Type[BaseModel], key: str) -> bool:
    if key in model.__annotations__:
        annotation = model.__annotations__[key]
        if get_origin(annotation) is list:
            return True

        if get_origin(annotation) in {Optional, Union}:
            args = get_args(annotation)
            return any(get_origin(arg) is list for arg in args)
    return False


def get_array_item_type(model: Type[BaseModel], key: str) -> str | None:
    type_map = {"str": "string", "int": "integer"}
    if not is_array(model, key):
        raise Exception(f"{key} is not an array")
    field = model.__annotations__[key]
    if get_origin(field) is list:
        return type_map[get_args(field)[0].__name__]
    elif get_origin(field) in {Optional, Union}:
        args = get_args(field)
        for arg in args:
            if get_origin(arg) is list:
                return type_map[get_args(arg)[0].__name__]
    return None


def is_enum_array(model: Type[BaseModel], key: str) -> bool:
    enum_type = get_array_item_enum_type(model, key)
    return issubclass(enum_type, Enum) if enum_type is not None else False


def get_enum_type_from_annotation(field) -> Type[Enum] | None:
    enum_type = None
    if get_origin(field) is list:
        enum_type = get_args(field)[0]
    elif get_origin(field) in {Optional, Union}:
        args = get_args(field)
        for arg in args:
            if get_origin(arg) is list:
                enum_type = get_args(arg)[0]
    if enum_type and issubclass(enum_type, Enum):
        return enum_type
    return None


def get_array_item_enum_type(model: Type[BaseModel], key: str) -> Type | None:
    if not is_array(model, key):
        return None
    field = model.__annotations__[key]
    return get_enum_type_from_annotation(field)


def get_enum_array_values(
    model: Type[BaseModel],
    key: str,
) -> List[str] | List[int]:
    if not is_enum_array(model, key):
        raise Exception(f"{key} is not an array of Enums")
    field = model.__annotations__[key]
    enum_type = get_enum_type_from_annotation(field)
    if enum_type:
        return [e.value for e in enum_type.__members__.values()]
    return []


def get_default_value(model: Type[BaseModel], key: str) -> Any:
    if is_enum(model, key):
        default_value = model.__fields__[key].default
        if is_enum(model, key) and isinstance(default_value, Enum):
            return default_value.value
        return default_value

    if key in model.__fields__:
        default_value = model.__fields__[key].default
        if default_value == "None" or default_value is None:
            return None
        return default_value

    return None
