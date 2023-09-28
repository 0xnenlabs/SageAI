from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from sageai.types.function import Function


class UnitTypes(str, Enum):
    CELSIUS = "Celsius"
    FAHRENHEIT = "Fahrenheit"


class FunctionInput(BaseModel):
    location: str = Field(
        ..., description="The city, e.g. San Francisco"
    )
    unit: Optional[UnitTypes] = Field(
        UnitTypes.CELSIUS, description="The unit of temperature."
    )


class FunctionOutput(BaseModel):
    weather: str

    def __eq__(self, other):
        if not isinstance(other, FunctionOutput):
            return False
        return self.weather == other.weather


def get_current_weather(params: FunctionInput) -> FunctionOutput:
    weather = (
        f"The weather in {params.location} is currently 22 degrees {params.unit.value}."
    )

    return FunctionOutput(weather=weather)


function = Function(
    function=get_current_weather,
    description="Get the current weather in a given location.",
)
