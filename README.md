# OpenAI Function Calling

Helper functions to generate OpenAI ChatGPT function calling requests. See the [official Function Calling reference](https://platform.openai.com/docs/guides/gpt/function-calling) for more information.

## Installation

Install from PyPi with:

```bash
pip install openai-function-calling
```

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
