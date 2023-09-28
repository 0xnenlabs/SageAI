from sageai.types.function import Function
from types import FunctionInput, FunctionOutput


def some_helper(params: FunctionInput) -> str:
    return (
        f"The weather {params.forecast} in {params.location} is going to be 22 degrees."
    )


def get_forecast_weather(params: FunctionInput) -> FunctionOutput:
    forecast = some_helper(params)
    return FunctionOutput(forecast=forecast)


function = Function(
    function=get_forecast_weather,
    description="Get the forecasted weather in a given location.",
)
