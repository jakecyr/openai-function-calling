from openai_function_calling.parameter import Parameter
from openai_function_calling.function import Function, FunctionDict

expected: dict = {
    "name": "get_current_weather",
    "description": "Get the current weather",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA",
            },
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["location"],
    },
}


def test_function_to_dict() -> None:
    location_parameter = Parameter(
        "location", "string", "The city and state, e.g. San Francisco, CA"
    )
    unit_parameter = Parameter("unit", "string", "", enum=["celsius", "fahrenheit"])

    get_current_weather_function = Function(
        "get_current_weather",
        "Get the current weather",
        [location_parameter, unit_parameter],
    )

    get_current_weather_function_dict: FunctionDict = (
        get_current_weather_function.to_dict()
    )

    assert get_current_weather_function_dict == expected
