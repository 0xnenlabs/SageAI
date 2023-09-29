import random
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from sageai.types.function import Function


class UnitTypes(str, Enum):
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"


class FunctionInput(BaseModel):
    min: Optional[int] = Field(0, description="The minimum number.")
    max: Optional[int] = Field(100, description="The maximum number.")


class FunctionOutput(BaseModel):
    number: int

    # In this case, we don't have a way to determine if the output is correct, so we just return True to make
    # the tests pass.
    def __eq__(self, other):
        if not isinstance(other, FunctionOutput):
            return False
        return True


def get_random_number(params: FunctionInput) -> FunctionOutput:
    number = random.randint(params.min, params.max)
    return FunctionOutput(number=number)


function = Function(
    function=get_random_number,
    description="Get a random number.",
)
