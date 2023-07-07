"""Weather Example.

Uses the function calling wrappers to decide between two functions
and extract entities to pass into the chosen function as arguments.
"""

import json
from collections.abc import Callable
from typing import Any

import openai

from openai_function_calling import FunctionInferer


# Define our functions.
def get_current_weather(location: str, unit: str) -> str:
    """Get the current weather and return a summary."""
    return f"It is currently sunny in {location} and 75 degrees {unit}."


def get_tomorrows_weather(location: str, unit: str) -> str:
    """Get tomorrow's weather and return a summary."""
    return f"It will be rainy tomorrow in {location} and around 65 degrees {unit}."


get_current_weather_schema = FunctionInferer.infer_from_function_reference(
    get_current_weather,
).to_json_schema()

get_tomorrows_weather_schema = FunctionInferer.infer_from_function_reference(
    get_tomorrows_weather,
).to_json_schema()


# Send the query and our function context to OpenAI.
response: Any = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {
            "role": "user",
            "content": "What will the weather be tomorrow in Boston MA in celsius?",
        },
    ],
    functions=[get_current_weather_schema, get_tomorrows_weather_schema],
    function_call="auto",  # Auto is the default.
)

response_message = response["choices"][0]["message"]

# Check if GPT wants to call a function.
if response_message.get("function_call"):
    # Call the function.
    available_functions: dict[str, Callable] = {
        "get_current_weather": get_current_weather,
        "get_tomorrows_weather": get_tomorrows_weather,
    }

    function_name = response_message["function_call"]["name"]
    function_args = json.loads(response_message["function_call"]["arguments"])
    function_to_call: Callable = available_functions[function_name]
    function_response: Any = function_to_call(**function_args)

    print(f"Called {function_name} with response: '{function_response!s}'.")
else:
    print("GPT does not want to called a function for the given query.")
