from pydantic import BaseModel, Field

from sageai.types.function import Function


class FunctionInput(BaseModel):
    location: str = Field(
        ..., description="The city and state, e.g. San Francisco, CA."
    )
    forecast: str = Field(..., description="The forecast, e.g. today, tomorrow.")


class FunctionOutput(BaseModel):
    forecast: str


def get_forecast_weather(params: FunctionInput) -> FunctionOutput:
    forecast = f"The weather {params.forecast} in {params.location} is going to be 22 degrees Celsius."
    return FunctionOutput(forecast=forecast)


function = Function(
    function=get_forecast_weather,
    description="Get the forecasted weather in a given location.",
)
