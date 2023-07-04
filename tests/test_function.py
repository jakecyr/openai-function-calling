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


def test_from_reference_returns_a_new_function() -> None:
    def sum(a: int, b: int) -> int:
        """Calculate the sum of integers and return the result.

        Args:
            a (int): The first integer to sum.
            b (int): The second integer to sum.

        Returns:
            int: _description_
        """
        return a + b

    function_definition: Function = Function.from_function(sum)

    assert isinstance(function_definition, Function)

    assert function_definition.name == "sum"
    assert (
        function_definition.description
        == "Calculate the sum of integers and return the result."
    )
    assert len(function_definition.parameters) == 2
    assert function_definition.parameters[0].name == "a"
    assert function_definition.parameters[1].name == "b"
    assert function_definition.parameters[0].type == "integer"
    assert function_definition.parameters[1].type == "integer"
    assert function_definition.parameters[0].description == "The first integer to sum."
    assert function_definition.parameters[1].description == "The second integer to sum."


def test_from_reference_without_docstring_with_type_hints_return_expected_values() -> (
    None
):
    def sum(a: int, b: int) -> int:
        return a + b

    function_definition: Function = Function.from_function(sum)

    assert isinstance(function_definition, Function)

    assert function_definition.name == "sum"
    assert function_definition.description == ""
    assert len(function_definition.parameters) == 2
    assert function_definition.parameters[0].name == "a"
    assert function_definition.parameters[1].name == "b"
    assert function_definition.parameters[0].type == "integer"
    assert function_definition.parameters[1].type == "integer"


def test_from_reference_with_no_type_hints_or_docstrings_still_returns_parameters() -> (
    None
):
    def sum(a, b) -> int:
        return a + b

    function_definition: Function = Function.from_function(sum)

    assert isinstance(function_definition, Function)

    assert function_definition.name == "sum"
    assert function_definition.description == ""
    assert len(function_definition.parameters) == 2
    assert function_definition.parameters[0].name == "a"
    assert function_definition.parameters[1].name == "b"


def test_from_reference_with_only_type_hints_returns_expected_parameters() -> None:
    def sum(a: int, b: int) -> int:
        return a + b

    function_definition: Function = Function.from_function(sum)

    assert isinstance(function_definition, Function)

    assert function_definition.name == "sum"
    assert function_definition.description == ""
    assert len(function_definition.parameters) == 2
    assert function_definition.parameters[0].name == "a"
    assert function_definition.parameters[0].type == "integer"
    assert function_definition.parameters[1].name == "b"
    assert function_definition.parameters[1].type == "integer"


def test_from_reference_with_only_docstring_no_types_returns_parameters_with_null_types() -> (
    None
):
    def sum(a, b) -> int:
        """
        Args:
            a: The first integer value.
            b: The second integer value.
        """
        return a + b

    function_definition: Function = Function.from_function(sum)

    assert isinstance(function_definition, Function)

    assert function_definition.name == "sum"
    assert len(function_definition.parameters) == 2
    assert function_definition.parameters[0].name == "a"
    assert function_definition.parameters[0].type == "null"
    assert function_definition.parameters[0].description == "The first integer value."
    assert function_definition.parameters[1].name == "b"
    assert function_definition.parameters[1].type == "null"
    assert function_definition.parameters[1].description == "The second integer value."


def test_from_reference_with_only_docstring_with_types_returns_parameters_with_defined_types() -> (
    None
):
    def sum(a, b) -> int:
        """Sums two values.

        Args:
            a (integer): The first integer value.
            b (integer): The second integer value.
        """
        return a + b

    function_definition: Function = Function.from_function(sum)

    assert isinstance(function_definition, Function)

    assert function_definition.name == "sum"
    assert function_definition.description == "Sums two values."
    assert len(function_definition.parameters) == 2
    assert function_definition.parameters[0].name == "a"
    assert function_definition.parameters[0].type == "integer"
    assert function_definition.parameters[0].description == "The first integer value."
    assert function_definition.parameters[1].name == "b"
    assert function_definition.parameters[1].type == "integer"
    assert function_definition.parameters[1].description == "The second integer value."


def test_from_reference_with_type_hints_and_docstring_without_types_returns_parameter_with_types_and_descriptions() -> (
    None
):
    def sum(a: float, b: float) -> float:
        """
        Args:
            a: The first float value.
            b: The second float value.
        """
        return a + b

    function_definition: Function = Function.from_function(sum)

    assert isinstance(function_definition, Function)

    assert function_definition.name == "sum"
    assert function_definition.description == ""
    assert len(function_definition.parameters) == 2
    assert function_definition.parameters[0].name == "a"
    assert function_definition.parameters[0].type == JsonSchemaType.NUMBER
    assert function_definition.parameters[0].description == "The first float value."
    assert function_definition.parameters[1].name == "b"
    assert function_definition.parameters[1].type == JsonSchemaType.NUMBER
    assert function_definition.parameters[1].description == "The second float value."


def test_from_reference_with_no_parameters_throws_returns_empty_parameters_list() -> (
    None
):
    def do_something() -> None:
        pass

    function_definition: Function = Function.from_function(do_something)

    assert isinstance(function_definition, Function)

    assert function_definition.name == "do_something"
    assert function_definition.description == ""
    assert len(function_definition.parameters) == 0
