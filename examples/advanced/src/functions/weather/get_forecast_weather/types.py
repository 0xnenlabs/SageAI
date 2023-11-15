from pydantic import BaseModel, Field


class FunctionInput(BaseModel):
    location: str = Field(..., description="The city, e.g. San Francisco")
    forecast: str = Field(..., description="The forecast, e.g. today, tomorrow.")


class FunctionOutput(BaseModel):
    forecast: str

    def __eq__(self, other):
        if not isinstance(other, FunctionOutput):
            return False
        return self.forecast == other.forecast
