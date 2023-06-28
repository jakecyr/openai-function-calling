"""Test the Function class."""

import pytest

from openai_function_calling.function import Function, FunctionDict
from openai_function_calling.json_schema_type import JsonSchemaType
from openai_function_calling.parameter import Parameter


def test_function_to_json_schema_returns_expected_dict() -> None:
    expected_dict: FunctionDict = {
        "name": "get_current_weather",
        "description": "Get the current weather",
        "parameters": {
            "type": JsonSchemaType.OBJECT,
            "properties": {
                "location": {
                    "type": JsonSchemaType.STRING,
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {
                    "type": JsonSchemaType.STRING,
                    "enum": ["celsius", "fahrenheit"],
                },
            },
        },
    }
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

    get_current_weather_function_dict: FunctionDict = (
        get_current_weather_function.to_json_schema()
    )

    assert get_current_weather_function_dict == expected_dict


def test_to_json_schema_with_required_parameters_adds_to_json_schema() -> None:
    required_parameters: list[str] = ["location"]

    location_parameter = Parameter(
        "location",
        JsonSchemaType.STRING,
        "The city and state, e.g. San Francisco, CA",
    )
    unit_parameter = Parameter(
        "unit",
        JsonSchemaType.STRING,
        "",
        enum=["celsius", "fahrenheit"],
    )
    get_current_weather_function = Function(
        "get_current_weather",
        "Get the current weather",
        [location_parameter, unit_parameter],
        required_parameters=required_parameters,
    )
    get_current_weather_function_dict: FunctionDict = (
        get_current_weather_function.to_json_schema()
    )

    assert (
        get_current_weather_function_dict["parameters"].get("required")
        == required_parameters
    )


def test_init_with_required_parameter_not_defined_raises_value_error() -> None:
    required_parameters: list[str] = ["location"]

    unit_parameter = Parameter(
        "unit",
        JsonSchemaType.STRING,
        "",
        enum=["celsius", "fahrenheit"],
    )

    with pytest.raises(
        ValueError,
        match=(
            f"Cannot require a parameter, '{required_parameters[0]}', "
            "that is not defined."
        ),
    ):
        Function(
            "get_current_weather",
            "Get the current weather",
            [unit_parameter],
            required_parameters=required_parameters,
        )


def test_to_json_schema_with_required_parameter_not_defined_raises_value_error() -> (
    None
):
    required_parameters: list[str] = ["location"]

    unit_parameter = Parameter(
        "unit",
        JsonSchemaType.STRING,
        "",
        enum=["celsius", "fahrenheit"],
    )
    get_current_weather_function = Function(
        "get_current_weather",
        "Get the current weather",
        [unit_parameter],
    )

    get_current_weather_function.required_parameters = required_parameters

    with pytest.raises(
        ValueError,
        match=(
            f"Cannot require a parameter, '{required_parameters[0]}', "
            "that is not defined."
        ),
    ):
        get_current_weather_function.to_json_schema()


def test_function_to_json_schema_without_parameters_returns_empty_dict() -> None:
    get_current_weather_function = Function(
        "get_current_weather",
        "Get the current weather",
    )

    get_current_weather_function_dict: FunctionDict = (
        get_current_weather_function.to_json_schema()
    )

    assert get_current_weather_function_dict["parameters"]["properties"] == {}
