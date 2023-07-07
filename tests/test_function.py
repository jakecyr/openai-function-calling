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


def test_to_dict_returns_same_value_as_to_json_schema() -> None:
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

    assert (
        get_current_weather_function.to_json_schema()
        == get_current_weather_function.to_dict()
    )


def test_merge_adds_new_values() -> None:
    get_current_weather_function = Function(
        name="get_current_weather",
        description="Get the current weather",
        parameters=[],
        required_parameters=[],
    )
    unit_parameter = Parameter(
        name="unit",
        type=JsonSchemaType.STRING,
        enum=["celsius", "fahrenheit"],
    )
    get_tomorrows_weather_function = Function(
        name="get_tomorrows_weather",
        description="Get the weather for tomorrow",
        parameters=[unit_parameter],
        required_parameters=["unit"],
    )

    get_current_weather_function.merge(get_tomorrows_weather_function)

    assert len(get_current_weather_function.parameters) == 1
    assert len(get_current_weather_function.required_parameters) == 1


def test_merge_does_not_replace_existing_values() -> None:
    get_current_weather_function = Function(
        name="get_current_weather",
        description="Get the current weather",
        parameters=[],
        required_parameters=[],
    )
    unit_parameter = Parameter(
        name="unit",
        type=JsonSchemaType.STRING,
        enum=["celsius", "fahrenheit"],
    )
    get_tomorrows_weather_function = Function(
        name="get_tomorrows_weather",
        description="Get the weather for tomorrow",
        parameters=[unit_parameter],
        required_parameters=["unit"],
    )

    get_current_weather_function.merge(get_tomorrows_weather_function)

    assert get_current_weather_function.name == "get_current_weather"
    assert get_current_weather_function.description == "Get the current weather"


def test_merge_adds_new_values_to_parameters() -> None:
    unit_parameter_old = Parameter(
        name="unit",
        type=JsonSchemaType.NULL,
    )
    get_current_weather_function = Function(
        name="get_current_weather",
        description="Get the current weather",
        parameters=[unit_parameter_old],
        required_parameters=[],
    )
    unit_parameter_new = Parameter(
        name="unit",
        type=JsonSchemaType.STRING,
        enum=["celsius", "fahrenheit"],
    )
    get_tomorrows_weather_function = Function(
        name="get_tomorrows_weather",
        description="Get the weather for tomorrow",
        parameters=[unit_parameter_new],
        required_parameters=["unit"],
    )

    get_current_weather_function.merge(get_tomorrows_weather_function)

    assert get_current_weather_function.parameters[0].enum == ["celsius", "fahrenheit"]
    assert get_current_weather_function.parameters[0].type == JsonSchemaType.STRING
    assert get_current_weather_function.required_parameters == ["unit"]


def test_merge_with_different_parameter_count_adds_parameter() -> None:
    unit_parameter_old = Parameter(
        name="unit",
        type=JsonSchemaType.NULL,
    )
    get_current_weather_function = Function(
        name="get_current_weather",
        description="Get the current weather",
        parameters=[unit_parameter_old],
        required_parameters=[],
    )
    unit_parameter_new = Parameter(
        name="unit",
        type=JsonSchemaType.STRING,
        enum=["celsius", "fahrenheit"],
    )
    get_tomorrows_weather_function = Function(
        name="get_tomorrows_weather",
        description="Get the weather for tomorrow",
        parameters=[unit_parameter_new],
        required_parameters=["unit"],
    )

    get_current_weather_function.merge(get_tomorrows_weather_function)

    assert get_current_weather_function.parameters[0].enum == ["celsius", "fahrenheit"]
    assert get_current_weather_function.parameters[0].type == JsonSchemaType.STRING
    assert get_current_weather_function.required_parameters == ["unit"]


def test_merge_with_same_parameters_does_not_change() -> None:
    unit_parameter = Parameter(
        name="unit",
        type=JsonSchemaType.NULL,
    )
    get_current_weather_function = Function(
        name="get_current_weather",
        description="Get the current weather",
        parameters=[unit_parameter],
        required_parameters=["unit"],
    )
    unit_parameter_new = Parameter(
        name=unit_parameter.name,
        type=JsonSchemaType.NULL,
    )
    get_tomorrows_weather_function = Function(
        name="get_tomorrows_weather",
        description="Get the weather for tomorrow",
        parameters=[unit_parameter_new],
        required_parameters=["unit"],
    )

    get_current_weather_function.merge(get_tomorrows_weather_function)

    assert get_current_weather_function.parameters[0] == Parameter(
        name="unit",
        type=JsonSchemaType.NULL,
    )
    assert (
        get_current_weather_function.required_parameters
        == get_tomorrows_weather_function.required_parameters
    )


def test_merge_with_no_name_sets_name() -> None:
    get_current_weather_function = Function(None, None)  # type: ignore
    get_tomorrows_weather_function = Function(
        name="get_tomorrows_weather",
        description="Get the weather for tomorrow",
    )

    get_current_weather_function.merge(get_tomorrows_weather_function)

    assert get_current_weather_function.name == get_tomorrows_weather_function.name
    assert (
        get_current_weather_function.description
        == get_tomorrows_weather_function.description
    )


def test_merge_with_no_parameters_does_not_add_any() -> None:
    get_current_weather_function = Function(
        name="get_current_weather",
        description="Get the current weather",
    )
    get_tomorrows_weather_function = Function(
        name="get_tomorrows_weather",
        description="Get the weather for tomorrow",
    )

    get_current_weather_function.merge(get_tomorrows_weather_function)

    assert len(get_current_weather_function.parameters) == 0
