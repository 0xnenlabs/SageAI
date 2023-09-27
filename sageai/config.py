from enum import Enum
import logging
from typing import Optional

from pydantic import BaseModel, ValidationError, Field
from sageai.services.default_vectordb_service import DefaultVectorDBService
from sageai.types.abstract_vectordb import AbstractVectorDB
from sageai.types.log_level import LogLevel

from sageai.utils.format_config_args import format_config_args


class Config(BaseModel):
    openai_key: str
    functions_directory: Optional[str] = Field(
        "functions", description="The directory of functions."
    )
    vectordb: Optional[AbstractVectorDB] = Field(
        DefaultVectorDBService, description="VectorDB class reference."
    )
    log_level: Optional[LogLevel] = Field(
        LogLevel.ERROR, description="The desired log level for output."
    )

    class Config:
        arbitrary_types_allowed = True


_config = Config(openai_key="")


def set_config(**kwargs):
    """Set the configuration parameters."""
    global _config
    try:
        kwargs = format_config_args(**kwargs)
        _config = Config(**kwargs)
        return _config
    except ValidationError as e:
        raise ValidationError(f"Invalid configuration: {e}")


def get_config():
    """Retrieve the configuration."""
    return _config
