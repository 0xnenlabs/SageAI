from typing import Optional

from pydantic import BaseModel, ValidationError, Field

from sageai.utils import format_config_args


class Config(BaseModel):
    openai_key: str
    functions_directory: Optional[str] = Field("functions", description="The directory of functions.")
    function_calling_model: Optional[str] = Field("gpt-3.5-turbo-0613",
                                                  description="The OpenAI model to use for function calling.")
    embeddings_model: Optional[str] = Field("text-embedding-ada-002",
                                            description="The OpenAI model to use for embeddings.")


_config = Config(openai_key="OPENAI_API_KEY")  # TODO change this


def set_config(**kwargs):
    """Set the configuration parameters."""
    global _config
    try:
        kwargs = format_config_args(kwargs)
        _config = Config(**kwargs)
    except ValidationError as e:
        raise ValidationError(f"Invalid configuration: {e}")


def get_config():
    """Retrieve the configuration."""
    return _config
