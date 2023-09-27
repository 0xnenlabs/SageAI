![Logo](https://github.com/0xnenlabs/SageAI/assets/45445790/750fb3f9-0830-4948-9a86-61e59d933b45)

<p align="center">
    <em>File-based functions for ChatGPT's function calling with Pydantic support 🚀</em>
</p>

<p align="center">
<a href="https://github.com/yezz123/ormdantic/actions/workflows/ci.yml" target="_blank">
    <img src="https://github.com/yezz123/ormdantic/actions/workflows/ci.yml/badge.svg" alt="Test">
</a>
<a href="https://codecov.io/gh/yezz123/ormdantic">
    <img src="https://codecov.io/gh/yezz123/ormdantic/branch/main/graph/badge.svg"/>
</a>
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
- CI/CD integration, ensuring synchronicity between your vector db and the functions directory.
- Minimalistic design with only two main dependencies: `openai` and `pydantic`.

## Requirements

```
python >=3.9, <3.12
pydantic >=1.6, <=1.10.12
openai ^0.28.1
```

## Installation

```bash
# pip
$ pip install sageai

# poetry
$ poetry add sageai
```

## Functions Format

```python
from typing import Optional

from pydantic import BaseModel, Field

from sageai.types.function import Function


class FunctionInput(BaseModel):
    location: str = Field(..., description="The city and state, e.g. San Francisco, CA.")


class FunctionOutput(BaseModel):
    weather: str


def get_current_weather(params: FunctionInput) -> FunctionOutput:
    weather = f"The weather in {params.location} is currently 22 degrees {params.unit}."
    return FunctionOutput(weather=weather)


function = Function(
    function=get_current_weather,
    description="Get the current weather in a given location.",
)
```

## Setup

Create a `functions` directory in the root directory, and add your functions as described in the section above. 

Then initalize `SageAI`.

```python
sageai = SageAI(openai_key="")
```

Then index the vector database.

```python
sageai.index()
```

That's it! Just start chatting 🚀

```python
message = "What's the weather like in Boston right now?"
response = sageai.chat(message=message)
# The weather in Boston, MA is currently 22 degreees celsius.
```

## Documentation

### SageAI.__init__()

Pass

### SageAI.index()

Pass

### SageAI.chat()

Pass

## Examples

- [basic](/examples/basic)
- [advanced](/examples/advanced)

## Roadmap

- Add tests
- Support streaming
- Support asyncio
- Add debug flag for logger
- Support Pydantic V2
- Write Chainlit example
- Write fullstack example

## Contributing

Please see our [CONTRIBUTING.md](/CONTRIBUTING.md).
