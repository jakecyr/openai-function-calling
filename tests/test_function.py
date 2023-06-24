"""Test the Function class."""

import pytest
from openai_function_calling.parameter import Parameter
from openai_function_calling.function import Function, FunctionDict


def test_function_to_dict_returns_expected_dict() -> None:
    expected_dict: FunctionDict = {
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
        },
    }
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

    assert get_current_weather_function_dict == expected_dict


def test_to_dict_with_required_parameters_adds_to_dict() -> None:
    required_parameters: list[str] = ["location"]

    location_parameter = Parameter(
        "location", "string", "The city and state, e.g. San Francisco, CA"
    )
    unit_parameter = Parameter("unit", "string", "", enum=["celsius", "fahrenheit"])
    get_current_weather_function = Function(
        "get_current_weather",
        "Get the current weather",
        [location_parameter, unit_parameter],
        required_parameters=required_parameters,
    )
    get_current_weather_function_dict: FunctionDict = (
        get_current_weather_function.to_dict()
    )

    assert (
        get_current_weather_function_dict["parameters"].get("required")
        == required_parameters
    )


def test_to_dict_with_required_parameter_not_defined_raises_value_error() -> None:
    required_parameters: list[str] = ["location"]

    unit_parameter = Parameter("unit", "string", "", enum=["celsius", "fahrenheit"])
    get_current_weather_function = Function(
        "get_current_weather",
        "Get the current weather",
        [unit_parameter],
        required_parameters=required_parameters,
    )

    with pytest.raises(ValueError):
        get_current_weather_function.to_dict()


def test_function_to_dict_without_parameters_returns_empty_dict() -> None:
    get_current_weather_function = Function(
        "get_current_weather",
        "Get the current weather",
    )

    get_current_weather_function_dict: FunctionDict = (
        get_current_weather_function.to_dict()
    )

    assert get_current_weather_function_dict["parameters"]["properties"] == {}
