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

```python
from openai_function_calling import Function, FunctionDict, Parameter

def get_current_weather(location: str, unit: str) -> str:
  # Do some stuff here...

# Define the function parameters.
location_parameter = Parameter(
    name="location",
    type="string",
    description="The city and state, e.g. San Francisco, CA"
)
unit_parameter = Parameter(
    name="unit",
    type="string",
    description="The temperature unit to use.",
    enum=["celsius", "fahrenheit"]
)

# Define the function.
get_current_weather_function = Function(
    "get_current_weather",
    "Get the current weather",
    [location_parameter, unit_parameter],
)

# Convert to a JSON schema dict to send to OpenAI.
get_current_weather_function_dict = get_current_weather_function.to_dict()

# Get the function to call from ChatGPT.
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
      {"role": "user", "content": "What will the weather be like in Boston, MA tomorrow?"}
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
