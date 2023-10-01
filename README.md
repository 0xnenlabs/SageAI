![Logo](https://github.com/0xnenlabs/SageAI/assets/45445790/750fb3f9-0830-4948-9a86-61e59d933b45)

<p align="center">
    <em>Folder-based functions for ChatGPT's function calling with Pydantic support 🚀</em>
</p>

<p align="center">
<a href="https://pypi.org/project/sageai" target="_blank">
    <img src="https://img.shields.io/pypi/v/sageai?label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/sageai" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/sageai.svg" alt="Supported Python versions">
</a>
</p>

SageAI is a framework for GPT 3.5/4 function calling for creating folder-based functions that is easy to organize and
scale.

With a built-in vector database used to store and retrieve functions, the number of tokens sent to the model is
significantly reduced, making it faster and cheaper to call your functions.

Read the blog post for a more in-depth explanation of the motivation behind SageAI [here](https://0xnen.com/blog/sageai).

## Table of Contents

- [Key Features](#key-features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Design](#design)
- [Setup](#setup)
- [Convention](#convention)
- [API](#api)
    - [SageAI Initialize](#sageai-initialize)
    - [SageAI Methods](#sageai-methods)
    - [Vector DB](#vector-db)
- [Testing](#testing)
    - [Unit Tests](#unit-tests)
    - [Integration Tests](#integration-tests)
    - [Output Equality](#output-equality)
    - [CLI](#cli)
- [Examples](#examples)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

## Key Features

- Function organization through folder-centric functions.
- Strong typing for functions using Pydantic.
- Built-in Qdrant vector database with in-memory support for function storage and retrieval, with the option to
  integrate your own.
- Easily test each function with an associated `test.json` file, supporting both unit and integration tests.
- Built with CI/CD in mind, ensuring synchronicity between your vector db and the functions directory across all
  environments using the `index` method.
- Lightweight implementation with only three dependencies:
    - `openai`
    - `pydantic`
    - `qdrant-client`

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

![Design](https://github.com/0xnenlabs/SageAI/assets/45445790/eb81d280-5b69-472a-b45a-4a9275fcf341)

SageAI is built around the concept of a `functions` directory, which contains all of your functions. Each function is
defined in a Python file `function.py`, and is associated with an optional `test.json` file for testing.

The format of the `function.py` file must contain two things in order for SageAI to work:

1. The function itself
2. The `Function` object

Input and output types may be defined using Pydantic models, and are automatically validated by SageAI. They can also be
defined outside the `function.py` file, and imported into the file.

Here is a simplified example of how SageAI might handle a function that fetches the current weather for a given
location.

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

That's it! You're now set up and ready to interact with SageAI through natural language queries. 🚀

```python
message = "What's the weather like in Toronto right now?"
response = sage.chat(
    messages=[dict(role="user", content=message)],
    model="gpt-3.5-turbo-0613",
    top_n=5,
)
# response:
# {
#   'name': 'get_current_weather',
#   'args': {'location': 'Toronto'},
#   'result': {'weather': 'The weather in Toronto is currently 22 degrees Celsius.'}
# }
```

## Convention

SageAI follows a convention over configuration approach to make it easy to define functions.

Ensure that your `function.py` file contains the following:

1. A `function` object that is an instance of `Function`.
2. A function that is the actual function that will be called by ChatGPT.
3. The function **must** have typed input and output Pydantic models.
4. Each field in the input model **must** have a description.

Minimal example:

```python
def my_function(params: PydanticInput) -> PydanticOutput:
    return PydanticOutput(...)


function = Function(
    function=my_function,
    description="My function description.",
)
```

## API

### SageAI Initialize

The `SageAI` constructor accepts the following parameters:

| Parameter               | Description                                                                 | Defaults                 |
|-------------------------|-----------------------------------------------------------------------------|--------------------------|
| **openai_key**          | The API key for OpenAI.                                                     | _Required_               |
| **functions_directory** | Directory containing functions.                                             | `/functions`             |
| **vectordb**            | An implementation of the `AbstractVectorDB` for vector database operations. | `DefaultVectorDBService` |
| **log_level**           | Desired log level for the operations.                                       | `ERROR`                  |

### SageAI Methods

#### 1. `chat`

Initiate a chat using OpenAI's API and the provided parameters.

**Parameters**:

| Parameter | Description                                                                                                         | Defaults   |
|-----------|---------------------------------------------------------------------------------------------------------------------|------------|
| -         | Accepts the same parameters as OpenAI's [chat endpoint](https://platform.openai.com/docs/api-reference/chat/create) | -          |
| **top_n** | The number of top functions to consider from the vector database.                                                   | _Required_ |

**Returns**:

```python
dict(
    name="function_name",
    args={"arg1": "value1", "arg2": "value2"},
    result={"out1": "value1", "out2": "value2"},  # Optional
    error="",  # Optional
)
```

> Either `result` or `error` will be present in the response, but not both.

---

#### 2. `get_top_n_functions`

Get the top `n` functions from the vector database based on a query.

**Parameters**:

| Parameter | Description                        | Defaults   |
|-----------|------------------------------------|------------|
| **query** | The query to search against.       | _Required_ |
| **top_n** | The number of functions to return. | _Required_ |

**Returns**:

- A dict of function names to `Function` definitions.

---

#### 3. `run_function`

Execute a function based on its name and provided arguments.

**Parameters**:

| Parameter | Description                        | Defaults   |
|-----------|------------------------------------|------------|
| **name**  | Name of the function.              | _Required_ |
| **args**  | Arguments to pass to the function. | _Required_ |

**Returns**:

- The function result as a dict.

---

#### 4. `call_openai`

Calls the OpenAI API with the provided parameters.

**Parameters**:

| Parameter         | Description                                                                                                         | Defaults   |
|-------------------|---------------------------------------------------------------------------------------------------------------------|------------|
| **openai_args**   | Accepts the same parameters as OpenAI's [chat endpoint](https://platform.openai.com/docs/api-reference/chat/create) | _Required_ |
| **top_functions** | List of dicts that is a representation of your functions.                                                           | _Required_ |

**Returns**:

- A tuple of the function name and the function args.

---

#### 5. `index`

Index the vector database based on the functions directory.
This method is useful to update the vectordb when new functions are added or existing ones are updated.

---

Want more control?

> The `chat` function uses `get_top_n_functions`, `run_function`, and `call_openai` internally.
> However, we also expose these methods incase you wish to use them directly to implement your own `chat` logic.

---

### Vector DB

SageAI comes with a built-in in-memory vector database, Qdrant, which is used to store and retrieve functions.

If you wish to use your own vector database, you can implement the `AbstractVectorDB` class and pass it into the
`SageAI` constructor.

See the [advanced example](/examples/advanced) for an example of how to integrate your own vector database.

## Testing

As for the optional `test.json` file in each function, follow this structure:

```json
[
  {
    "message": "What's the weather like in Toronto right now?",
    "input": {
      "location": "Toronto",
      "unit": "Celsius"
    },
    "output": {
      "weather": "The weather in Toronto is currently 22 degrees Celsius."
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

---

### Unit Tests

> Unit tests do not call the vector database nor ChatGPT, and **will not** cost you OpenAI credits.

- Unit tests are used to ensure your functions directory is valid, and it tests the function in isolation.
- It tests whether:
    - the `functions` directory exists.
    - each function has a `function.py` file.
    - each `function.py` file has a `Function` object.
    - and more!
- It also tests whether the input and output types are valid, and whether the function returns the expected output based
  on
  the input alone by calling `func(test_case["input"]) == test_case["output"]`.

---

### Integration Tests

> Integration tests will call the vector database and ChatGPT, and **will** cost you OpenAI credits.

- Integration tests are used to test the function by calling ChatGPT and the vector database.
- They test whether the vector database is able to retrieve the function, and whether ChatGPT can call the function
  with the given input and return the expected output.

> Because ChatGPT's responses can vary, integration tests may return different results each time.
> It's important to use integration tests as a tool to ensure ChatGPT is able to call the right function with the right
> input, and not as a definitive test to measure the test rate of your functions.

---

### Output Equality

You can customize how to determine equality between the expected and actual output by overriding the `__eq__`
method in the output model.

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
against a subset of the fields (for example, the `id` field).

---

### CLI

```bash
# To run unit and integration tests for all functions:
poetry run sageai-tests --apikey=openapikey --directory=path/to/functions

# To run unit tests only for all functions:
poetry run sageai-tests --apikey=openapikey --directory=path/to/functions --unit

# To run integration tests only for all functions:
poetry run sageai-tests --apikey=openapikey --directory=path/to/functions --integration

# To run unit and integration tests for a specific function:
poetry run sageai-tests --apikey=openapikey --directory=path/to/functions/get_current_weather
```

| Parameter         | Description                                                   | Defaults     |
|-------------------|---------------------------------------------------------------|--------------|
| **--apikey**      | OpenAI API key.                                               | _Required_   |
| **--directory**   | Directory of the functions or of the specific function to run | _/functions_ |
| **--unit**        | Only run unit tests                                           | false        |
| **--integration** | Only run integration tests                                    | false        |

## Examples

1. [Basic](/examples/basic) - Get started with a simple SageAI function.
2. [Advanced](/examples/advanced) - Dive deeper with more intricate functionalities and use-cases.

## Roadmap

- [ ] Add tests and code coverage
- [ ] Support multiple function calls
- [ ] Support streaming
- [ ] Support asyncio
- [ ] Support Pydantic V2
- [ ] Write Chainlit example
- [ ] Write fullstack example

## Contributing

Interested in contributing to SageAI? Please see our [CONTRIBUTING.md](/CONTRIBUTING.md) for guidelines, coding
standards, and other details.
