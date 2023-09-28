![Logo](https://github.com/0xnenlabs/SageAI/assets/45445790/750fb3f9-0830-4948-9a86-61e59d933b45)

<p align="center">
    <em>File-based functions for ChatGPT's function calling with Pydantic support 🚀</em>
</p>

<p align="center">
<a href="https://pypi.org/project/sageai" target="_blank">
    <img src="https://img.shields.io/pypi/v/sageai?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/sageai" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/sageai.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

## Key Features

- Organization through file-centric functions, organized in directories.
- Strong typing for functions using Pydantic.
- Built-in in-memory FAISS vector database, with the option to integrate your own.
- Easily test each function with an associated test.json file, supporting both unit and integration tests.
- Built with CI/CD in mind, ensuring synchronicity between your vector db and the functions directory across all
  environments.
- Lightweight implementation with only three dependencies: `openai`, `pydantic`, and `qdrant-client`.

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

## Functions Directory

SageAI is built around the concept of a `functions` directory, which contains all of your functions. Each function is
defined in a Python file `function.py`, and is associated with an optional `test.json` file for testing.

The format of the `function.py` file must contain two things in order for SageAI to work:

1. The function itself
2. The `Function` object

Input and output types may be defined using Pydantic models, and are automatically validated by SageAI. They can also be
defined outside the `function.py` file, and imported into the file.

Below is a minimal example of a function that returns the current weather in a given location.

```python
# function.py
from pydantic import BaseModel, Field

from sageai.types.function import Function


class FunctionInput(BaseModel):
    location: str = Field(
        ...,
        # Required, will be used in the request to OpenAI
        description="The city and state, e.g. San Francisco, CA."
    )


class FunctionOutput(BaseModel):
    weather: str


def get_current_weather(params: FunctionInput) -> FunctionOutput:
    weather = (
        f"The weather in {params.location} is currently 22 degrees {params.unit.value}."
    )
    return FunctionOutput(weather=weather)


function = Function(
    function=get_current_weather,
    # Required, will be used in the request to OpenAI
    description="Get the current weather in a given location.",
)
```

As for the `test.json` file,

## Setup

Create a `functions` directory in the root directory, and add your functions as described in the section above.

Then initialize `SageAI`.

```python
from sageai import SageAI

sageai = SageAI(openai_key="")
```

Then index the vector database.

```python
sageai.index()
```

That's it! Just start chatting 🚀

```python
message = "What's the weather like in Boston right now?"
response = sageai.chat(
    messages=[dict(role="user", content=message)],
    model="gpt-3.5-turbo-0613",
    sageai=dict(k=5),
)
# The weather in Boston, MA is currently 22 degrees Celsius.
```

## Documentation

### SageAI.__init__()

Pass

### SageAI.index()

Pass

### SageAI.chat()

Pass

## Examples

- [basic](/examples/1-basic)
- [advanced](/examples/2-advanced)

## Limitations

## Roadmap

- Add tests and code coverage
- Support streaming
- Support asyncio
- Add debug flag for logger
- Support Pydantic V2
- Write Chainlit example
- Write fullstack example

## Contributing

Please see our [CONTRIBUTING.md](/CONTRIBUTING.md).
