![Logo](https://github.com/0xnenlabs/SageAI/assets/45445790/750fb3f9-0830-4948-9a86-61e59d933b45)

<p align="center">
    <em>Folder-based functions for ChatGPT's function calling with Pydantic support 🚀</em>
</p>

<p align="center">
<a href="https://pypi.org/project/sageai" target="_blank">
    <img src="https://img.shields.io/pypi/v/sageai?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/sageai" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/sageai.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

## Table of Contents

- [Key Features](#key-features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Design](#design)
- [Setup](#setup)
- [API](#api)
  * [SageAI Setup](#sageai-setup)
  * [SageAI Methods](#sageai-methods)
- [Testing](#testing)
  * [Unit Tests](#unit-tests)
  * [Integration Tests](#integration-tests)
  * [Output Equality](#output-equality)
  * [CLI](#cli)
- [Examples](#examples)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

## Key Features

- Function organization through folder-centric functions.
- Strong typing for functions using Pydantic.
- Built-in in-memory Qdrant vector database for function storage and retrieval, with the option to integrate your own.
- Easily test each function with an associated `test.json` file, supporting both unit and integration tests.
- Built with CI/CD in mind, ensuring synchronicity between your vector db and the functions directory across all
  environments using the `index` method.
- Lightweight implementation with only four dependencies: `openai`, `pydantic`, `qdrant-client`, and `pytest`.

## Requirements

```
python >=3.9, <3.12
pydantic >=1.6, <=1.10.12
openai >=0.27.0
qdrant-client >=1.4.0
```

## Installation

```bash
# pip
$ pip install sageai

# poetry
$ poetry add sageai
```

## Design

SageAI is built around the concept of a `functions` directory, which contains all of your functions. Each function is
defined in a Python file `function.py`, and is associated with an optional `test.json` file for testing.

The format of the `function.py` file must contain two things in order for SageAI to work:

1. The function itself
2. The `Function` object

Input and output types may be defined using Pydantic models, and are automatically validated by SageAI. They can also be
defined outside the `function.py` file, and imported into the file.

Below is a minimal example of a function that returns the current weather in a given location.

```python
# functions/get_current_weather/function.py
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from sageai.types.function import Function


class UnitTypes(str, Enum):
    CELSIUS = "Celsius"
    FAHRENHEIT = "Fahrenheit"


class FunctionInput(BaseModel):
    location: str = Field(
        ..., description="The city and state, e.g. San Francisco, CA."
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
```

We'll break down the above example into its components below.

## Setup

Create a `functions` directory in the root directory, and add your functions as described in [Design](#design).

Then initialize `SageAI`.

```python
from sageai import SageAI

sage = SageAI(openai_key="")
```

Then index the vector database.

```python
sage.index()
```

That's it! Just start chatting 🚀

```python
message = "What's the weather like in Boston right now?"
response = sageai.chat(
    messages=[dict(role="user", content=message)],
    model="gpt-3.5-turbo-0613",
    top_n=5,
)
# {
#   'name': 'get_current_weather', 
#   'args': {'location': 'Boston, MA'}, 
#   'result': {'weather': 'The weather in Boston, MA is currently 22 degrees Celsius.'}
# }
```

## API

### SageAI Setup

To instantiate the `SageAI` class, you need:

- **openai_key**: The API key for OpenAI.
- **functions_directory** (optional): Directory containing functions.
- **vectordb** (optional): An implementation of the `AbstractVectorDB` for vector database operations.
- **log_level** (optional): Desired log level for the operations.

### SageAI Methods

#### `chat`

Initiate a chat using OpenAI's API and the provided parameters.
The method handles fetches similar functions from the vector database, calls OpenAI and runs appropriate function.

**Parameters**:

- Accepts the same parameters as OpenAI's [chat endpoint](https://platform.openai.com/docs/api-reference/chat/create)
- **top_n** (required): The number of top functions to consider from the vector database.

**Returns**:

- A dict containing the function name, arguments, result, and error.

```python
dict(
    name="function_name",
    args={"arg1": "value1", "arg2": "value2"},
    result={"out1": "value1", "out2": "value2"},  # Optional
    error="",  # Optional
)
```

Either `result` or `error` will be present in the response, but not both.

#### `get_top_n_functions`

Get the top `n` functions from the vector database based on a query.

**Parameters**:

- **query**: The query to search against.
- **top_n**: The number of functions to return.

**Returns**:

- A dict of function names to `Function` definitions.

#### `run_function`

Execute a function based on its name and provided arguments.

**Parameters**:

- **name**: Name of the function.
- **args**: Arguments to pass to the function.

**Returns**:

- The function result.

#### `index`

Index the vector database based on the functions directory.
This method is useful to update the vectordb when new functions are added or existing ones are updated.

## Testing

As for the optional `test.json` file in each function, follow this structure:

```json
[
  {
    "message": "What's the weather like in Boston right now?",
    "input": {
      "location": "Boston",
      "unit": "Celsius"
    },
    "output": {
      "weather": "The weather in Boston, MA is currently 22 degrees Celsius."
    }
  }
]
```

- Each object in the array represents a test case.
- The `message` field is the natural language message that will be sent
  to ChatGPT, and the `input` field is the expected input that will be passed to the function.
- The `output` field is the
  expected output of the function.

SageAI offers unit and integration tests.

### Unit Tests

- Unit tests are used to ensure your functions directory is valid, and it tests the function in isolation.
- It tests whether:
    - the `functions` directory exists,
    - each function has a `function.py` file,
    - each `function.py` file has a `Function` object
    - and more!
- It also tests whether the input and output types are valid, and whether the function returns the expected output based
  on
  the input alone by calling `func(test_case["input"]) == test_case["output"]`.

> Note that this does not call the vector database nor ChatGPT, and **WILL NOT** cost you money.

### Integration Tests

- Integration tests are used to test the function by calling ChatGPT and the vector database.
- They test whether the vector database is able to retrieve the function, and whether ChatGPT can call the function
  with the given input and return the expected output.

> Note that this will call the vector database and ChatGPT, and **WILL** cost you money.

### Output Equality

We let you determine equality between the expected output and the actual output by overriding the
`__eq__` method in the output model.

```python
class FunctionOutput(BaseModel):
    weather: str
    temperature: int

    def __eq__(self, other):
        if not isinstance(other, FunctionOutput):
            return False
        return self.weather == other.weather
```

In the case above, we only care about the `weather` field, and not the `temperature` field. Therefore, we only compare
the `weather` field in the `__eq__` method.

This is especially useful when you are returning an object from a database, for example, and you only care to test
against a subset of the fields.

### CLI

```bash
# To run unit and integration tests for all functions:
poetry run sageai-tests --directory=path/to/functions --apikey=openapi-key

# To run unit tests only for all functions:
poetry run sageai-tests --directory=path/to/functions --apikey=openapi-key --unit

# To run integration tests only for all functions:
poetry run sageai-tests --directory=path/to/functions --apikey=openapi-key --integration
```

To run tests for a specific function, simply give it the path to the function directory:

```bash
poetry run sageai-tests --directory=path/to/functions/get_current_weather --apikey=openapi-key
```

> Note that `--directory` defaults to `./functions`, and `--apikey` defaults to the `OPENAI_API_KEY` environment
> variable.

A note on integration tests:

> Because of the non-deterministic nature of ChatGPT, integration tests may return different results each time.
> It's important to use integration tests as a sanity check, and not as a definitive test.

## Examples

1. [Basic](/examples/1-basic)
2. [Advanced](/examples/2-advanced)

## Roadmap

- [ ] Add tests and code coverage
- [ ] Support multiple function calls
- [ ] Support streaming
- [ ] Support asyncio
- [ ] Support Pydantic V2
- [ ] Write Chainlit example
- [ ] Write fullstack example

## Contributing

Please see our [CONTRIBUTING.md](/CONTRIBUTING.md).
