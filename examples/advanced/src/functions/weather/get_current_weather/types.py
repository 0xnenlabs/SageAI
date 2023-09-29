from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class UnitTypes(str, Enum):
    CELSIUS = "Celsius"
    FAHRENHEIT = "Fahrenheit"


class FunctionInput(BaseModel):
    location: str = Field(..., description="The city, e.g. San Francisco")
    unit: Optional[UnitTypes] = Field(
        UnitTypes.CELSIUS, description="The unit of temperature."
    )


class FunctionOutput(BaseModel):
    weather: str

    def __eq__(self, other):
        if not isinstance(other, FunctionOutput):
            return False
        return self.weather == other.weather
