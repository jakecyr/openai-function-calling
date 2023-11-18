# OpenAI Function Calling

[![GitHub Actions Build Status](https://github.com/jakecyr/openai-function-calling/actions/workflows/test-application.yml/badge.svg)](https://github.com/jakecyr/openai-function-calling/actions)
[![PyPi Package Version](https://badge.fury.io/py/openai-function-calling.svg)](https://pypi.org/project/openai-function-calling/)

Helper functions to generate JSON schema dicts for OpenAI ChatGPT function calling requests. See the [official Function Calling reference](https://platform.openai.com/docs/guides/gpt/function-calling) for more information.

## Installation

Install from PyPi with:

```bash
pip install openai-function-calling
```

**The openai-function-calling package does come with the openai package. It must be installed separately with `pip install openai`**

## Usage

### Auto-Infer the Function Definition (Beta)

Automatically infer your function name, description, and parameters given a reference to the function. A `Function` instance is returned which can be converted to JSON schema with `.to_json_schema()` and then passed to the OpenAI chat completion API:

```python
from typing import Any, Callable
from openai_function_calling import FunctionInferrer
import openai
import json

# Define example functions.

def get_current_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the current weather and return a summary."""
    return f"It is currently sunny in {location} and 75 degrees {unit}."


def get_tomorrows_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the weather for tomorrow and return a summary."""
    return f"Tomorrow it will be rainy in {location} and 60 degrees {unit}."

# Infer the function definitions.
get_current_weather_function = FunctionInferrer.infer_from_function_reference(
    get_current_weather
)

get_tomorrows_weather_function = FunctionInferrer.infer_from_function_reference(
    get_tomorrows_weather
)

# Get the function to call from ChatGPT (you would normally have more than one).
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {
            "role": "user",
            "content": "What will the weather be like in Boston, MA today?",
        }
    ],
    functions=[
        # Convert the functions to JSON schema.
        get_current_weather_function.to_json_schema(),
        get_tomorrows_weather_function.to_json_schema(),
    ],
)
```

### Define Functions with Objects

Define your function definitions using typed classes `Function` and `Parameter` which automatically convert to JSON schema with `.to_json_schema` methods. See an example below:

```python
from openai_function_calling import Function, FunctionDict, Parameter, JsonSchemaType


def get_current_weather(location: str, unit: str) -> str:
    """Do some stuff in here."""


# Define the function.
get_current_weather_function = Function(
    "get_current_weather",
    "Get the current weather",
    [
        Parameter(
            name="location",
            type=JsonSchemaType.STRING,
            description="The city and state, e.g. San Francisco, CA",
        ),
        Parameter(
            name="unit",
            type=JsonSchemaType.STRING,
            description="The temperature unit to use.",
            enum=["celsius", "fahrenheit"],
        ),
    ],
)

# Convert to a JSON schema dict to send to OpenAI.
get_current_weather_function_schema = get_current_weather_function.to_json_schema()
```

### Convert Functions to OpenAI Compatible JSON

```python
from openai import OpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionUserMessageParam,
)
from openai_function_calling.tool_helpers import ToolHelpers


# Define our functions.
def get_current_weather(location: str, unit: str) -> str:
    """Get the current weather and return a summary."""
    return f"It is currently sunny in {location} and 75 degrees {unit}."


def get_tomorrows_weather(location: str, unit: str) -> str:
    """Get tomorrow's weather and return a summary."""
    return f"It will be rainy tomorrow in {location} and around 65 degrees {unit}."


openai_client = OpenAI()

# Send the query and our function context to OpenAI.
response: ChatCompletion = openai_client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        ChatCompletionUserMessageParam(
            role="user", content="What's the weather in Boston MA?"
        ),
    ],
    tools=ToolHelpers.infer_from_function_refs(
        [get_current_weather, get_tomorrows_weather]
    ),
    tool_choice="auto",
)
```

## Examples

To run the examples, set the environment variable `OPENAI_API_KEY` to your OpenAI API key. For example:

```bash
export OPENAI_API_KEY=SOME_KEY_VALUE

# or when running an example

OPENAI_API_KEY=SOME_KEY_VALUE python examples/weather_functions.py
```

Make sure to also follow all instructions in the [Installation section](#installation).

See complete examples in the [./examples](https://github.com/jakecyr/openai-function-calling/tree/master/examples) folder.
