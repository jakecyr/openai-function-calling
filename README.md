# OpenAI Function Calling

![GitHub Actions Build Status](https://github.com/jakecyr/openai-function-calling/actions/workflows/test-application.yml/badge.svg)

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
def get_current_weather(location: str, unit: str) -> str:
    """Get the current weather and return a summary."""
    return f"It is currently sunny in {location} and 75 degrees {unit}."

get_current_weather_json_schema = Function.from_function(get_current_weather).to_json_schema()

# Get the function to call from ChatGPT (you would normally have more than one).
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {
            "role": "user",
            "content": "What will the weather be like in Boston, MA today?",
        }
    ],
    functions=[get_current_weather_json_schema],
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
get_current_weather_function_dict = get_current_weather_function.to_json_schema()

# Get the function to call from ChatGPT.
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {
            "role": "user",
            "content": "What will the weather be like in Boston, MA tomorrow?",
        }
    ],
    functions=[get_current_weather_function_dict],
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
