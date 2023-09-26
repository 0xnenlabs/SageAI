import inspect
import os
from typing import Optional
from pydantic import BaseModel, Field, ValidationError, root_validator

from sageai.utils import format_config_args


class Config(BaseModel):
    functions_directory: Optional[str] = Field(
        None, description="File path to the functions directory"
    )
    openai_key: Optional[str] = Field(None, description="OpenAI key")
    function_calling_model: Optional[str] = Field(
        "gpt-3.5-turbo-0613",
        description="OpenAI model to use for function calling",
    )
    embeddings_model: Optional[str] = Field(
        "text-embedding-ada-002",
        description="OpenAI model to use for creating embeddings",
    )


_config = Config()


def set_config(**kwargs: "Config"):
    """Set the configuration parameters."""
    global _config
    try:
        kwargs = format_config_args(kwargs)
        _config = Config(**kwargs)
    except ValidationError as e:
        raise TypeError(f"Invalid configuration: {e}")


def get_config():
    """Retrieve the configuration."""
    return _config
