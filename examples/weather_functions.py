import json
from typing import Any, Callable
import openai
from openai_function_calling import Function, FunctionDict, Parameter


def get_current_weather(location: str, unit: str) -> str:
    return f"Called get_current_weather with location {location} and unit {unit}."


def get_tomorrows_weather(location: str, unit: str) -> str:
    return f"Called get_tomorrows_weather with location {location} and unit {unit}."


messages: list[dict[str, str]] = [
    {"role": "user", "content": "What will the weather be like in Boston, MA tomorrow?"}
]

location_parameter = Parameter(
    "location", "string", "The city and state, e.g. San Francisco, CA"
)
unit_parameter = Parameter("unit", "string", "", enum=["celsius", "fahrenheit"])
get_current_weather_function = Function(
    "get_current_weather",
    "Get the current weather",
    [location_parameter, unit_parameter],
)
get_tomorrows_weather_function = Function(
    "get_tomorrows_weather",
    "Get the tomorrow's weather",
    [location_parameter, unit_parameter],
)


get_current_weather_function_dict: FunctionDict = get_current_weather_function.to_dict()
get_tomorrows_weather_function_dict: FunctionDict = (
    get_tomorrows_weather_function.to_dict()
)

response: Any = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=messages,
    functions=[get_current_weather_function_dict, get_tomorrows_weather_function_dict],
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

    function_response: Any = function_to_call(
        location=function_args.get("location"),
        unit=function_args.get("unit"),
    )

    print(f"Called {function_name} with response: {function_response!s}")
