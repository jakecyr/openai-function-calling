"""Weather Example.

Uses the function calling wrappers to decide between two functions
and extract entities to pass into the chosen function as arguments.
"""

import json
from collections.abc import Callable
from typing import Any

import openai
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessage,
    ChatCompletionMessageToolCall,
    ChatCompletionUserMessageParam,
)

from openai_function_calling import Function, JsonSchemaType, Parameter
from openai_function_calling.tool_helpers import ToolHelpers


# Define our functions.
def get_current_weather(location: str, unit: str) -> str:
    return f"It is currently sunny in {location} and 75 degrees {unit}."


def get_tomorrows_weather(location: str, unit: str) -> str:
    return f"It will be rainy tomorrow in {location} and around 65 degrees {unit}."


# Convert our functions to JSON schema.
location_parameter = Parameter(
    name="location",
    type=JsonSchemaType.STRING,
    description="The city and state, e.g. San Francisco, CA",
)
unit_parameter = Parameter(
    name="unit",
    type=JsonSchemaType.STRING,
    enum=["celsius", "fahrenheit"],
)
get_current_weather_function = Function(
    name="get_current_weather",
    description="Get the current weather",
    parameters=[location_parameter, unit_parameter],
)
get_tomorrows_weather_function = Function(
    name="get_tomorrows_weather",
    description="Get the tomorrow's weather",
    parameters=[location_parameter, unit_parameter],
)


# Send the query and our function context to OpenAI.
response: ChatCompletion = openai.chat.completions.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        ChatCompletionUserMessageParam(
            role="user",
            content="What's the weather tomorrow in Boston MA in fahrenheit?",
        ),
    ],
    tools=ToolHelpers.from_functions(
        [
            get_current_weather_function,
            get_tomorrows_weather_function,
        ]
    ),
    tool_choice="auto",  # Auto is the default.
)

response_message: ChatCompletionMessage = response.choices[0].message


# Check if GPT wants to call a function.
if response_message.tool_calls is not None:
    # Call the function.
    available_functions: dict[str, Callable] = {
        "get_current_weather": get_current_weather,
        "get_tomorrows_weather": get_tomorrows_weather,
    }

    tool_call: ChatCompletionMessageToolCall = response_message.tool_calls[0]
    function = tool_call.function
    arguments: str = function.arguments
    function_name: str = tool_call.function.name

    function_args: dict = json.loads(arguments)
    function_reference: Callable = available_functions[function_name]
    function_response: Any = function_reference(**function_args)

    print(f"Called {function_name} with response: '{function_response!s}'.")
else:
    print("GPT does not want to called a function for the given query.")
