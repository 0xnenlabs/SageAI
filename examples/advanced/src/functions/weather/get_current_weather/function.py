from sageai.types.function import Function
from examples.advanced.src.functions.weather.get_current_weather.types import (
    FunctionInput,
    FunctionOutput,
)


def get_current_weather(params: FunctionInput) -> FunctionOutput:
    weather = (
        f"The weather in {params.location} is currently 22 degrees {params.unit.value}."
    )
    return FunctionOutput(weather=weather)


function = Function(
    function=get_current_weather,
    description="Get the current weather in a given location.",
)
