from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class Config(BaseModel):
    functions_path: str = Field(..., description="File path to the functions directory")
    openai_key: str = Field(..., description="OpenAI key")
    model: Optional[str] = Field(
        "gpt-3.5-turbo-0613",
        description="OpenAI model to use (has to support function-calling)",
    )


_config = Config()


def set_config(**kwargs: "Config"):
    """Set the configuration parameters."""
    global _config
    try:
        _config = Config(**kwargs)
    except ValidationError as e:
        raise TypeError(f"Invalid configuration: {e}")


def get_config():
    """Retrieve the configuration."""
    return _config
