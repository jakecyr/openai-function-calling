"""Weather Example.

Uses the function calling wrappers to decide between two functions
and extract entities to pass into the chosen function as arguments.
"""

import json
from collections.abc import Callable
from typing import Any

from openai import OpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessage,
    ChatCompletionUserMessageParam,
)
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
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
