"""Test the function inferrer class."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional

import pytest

from openai_function_calling import FunctionInferrer
from openai_function_calling.function import Function
from openai_function_calling.json_schema_type import JsonSchemaType


class TemperatureUnit(Enum):
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"


class Places(Enum):
    SAN_FRANCISCO = auto()
    NEW_YORK = auto()


@dataclass
class Location:
    city: Places
    state: str


def add_location(location: Location) -> None:
    """Add a location to the database.

    Args:
        location: The location to add to the database.

    """


def add_locations(locations: list[dict]) -> None:
    """Add a locations to the database.

    Args:
        locations: The list of locations to add.

    """


def add_generic_locations(locations: list) -> None:
    """Add a locations to the database.

    Args:
        locations: The list of locations to add.

    """


def add_generic_typing_locations(locations: list) -> None:
    """Add a locations to the database.

    Args:
        locations: The list of locations to add.

    """


def get_state_from_city(city: Places) -> str:
    """Get the state from a city.

    Args:
        city: The city to get the state for.

    Returns:
        The state of the city.

    """
    return "CA"


def fully_documented_sum(a: int, b: int) -> int:
    """Sum two values.

    Args:
        a: The first value to sum.
        b: The second value to sum.

    Returns:
        The sum of the two values.

    """
    return a + b


def no_docstring_sum(a: int, b: int) -> int:
    return a + b


def get_temperature(location: str, unit: TemperatureUnit) -> float:
    """Get the current temperature.

    Args:
        location: The location to get the temperature for.
        unit: The unit to return the temperature in.

    Returns:
        The current temperature in the specified unit.

    """
    return 75


def get_temperature_with_default(
    location: str,
    unit: TemperatureUnit = TemperatureUnit.CELSIUS,
) -> float:
    """Get the current temperature.

    Args:
        location: The location to get the temperature for.
        unit: The unit to return the temperature in.

    Returns:
        The current temperature in the specified unit.

    """
    return 75


def get_temperature_with_all_defaults(
    location: str = "Boston, MA",
    unit: TemperatureUnit = TemperatureUnit.CELSIUS,
) -> float:
    """Get the current temperature.

    Args:
        location: The location to get the temperature for.
        unit: The unit to return the temperature in.

    Returns:
        The current temperature in the specified unit.

    """
    return 75


def get_local_places_with_optional_location(
    location: Optional[str] = None,  # noqa: FA100
) -> list:
    """Get the current temperature.

    Args:
        location: The location to get the temperature for.

    Returns:
        The current temperature in the specified unit.

    """
    return []


def test_infer_from_function_reference_returns_a_function_instance() -> None:
    function: Function = FunctionInferrer.infer_from_function_reference(
        fully_documented_sum
    )

    assert isinstance(function, Function)


def test_infer_from_function_reference_returns_function_with_name_defined() -> None:
    function: Function = FunctionInferrer.infer_from_function_reference(
        fully_documented_sum
    )

    assert function.name == fully_documented_sum.__name__


def test_infer_from_function_reference_returns_function_with_description_defined() -> (
    None
):
    function: Function = FunctionInferrer.infer_from_function_reference(
        fully_documented_sum
    )

    assert function.description == "Sum two values."


def test_infer_from_function_reference_returns_function_with_expected_parameter_count() -> (
    None
):
    function: Function = FunctionInferrer.infer_from_function_reference(
        fully_documented_sum
    )

    assert len(function.parameters) == 2


def test_infer_from_function_reference_returns_function_with_expected_parameter_attributes() -> (
    None
):
    function: Function = FunctionInferrer.infer_from_function_reference(
        fully_documented_sum
    )

    assert function.parameters[0].name == "a"
    assert function.parameters[0].type == "integer"
    assert function.parameters[0].description == "The first value to sum."
    assert function.parameters[0].array_item_type is None
    assert function.parameters[0].enum is None

    assert function.parameters[1].name == "b"
    assert function.parameters[1].type == "integer"
    assert function.parameters[1].description == "The second value to sum."
    assert function.parameters[1].array_item_type is None
    assert function.parameters[1].enum is None


def test_infer_from_function_reference_returns_function_with_expected_values() -> None:
    function: Function = FunctionInferrer.infer_from_function_reference(
        no_docstring_sum
    )

    assert function.name == no_docstring_sum.__name__
    assert len(function.parameters) == 2
    assert function.parameters[0].name == "a"
    assert function.parameters[0].type == "integer"
    assert function.parameters[1].name == "b"
    assert function.parameters[1].type == "integer"


def test_infer_from_function_reference_with_enum_returns_function_with_enum() -> None:
    function: Function = FunctionInferrer.infer_from_function_reference(get_temperature)
    assert function.parameters[1].enum == ["celsius", "fahrenheit"]


def test_infer_from_function_reference_with_enum_returns_correct_value_type() -> None:
    function: Function = FunctionInferrer.infer_from_function_reference(
        get_state_from_city
    )
    assert function.parameters[0].type == JsonSchemaType.INTEGER.value


def test_infer_from_function_reference_with_dataclass_sets_as_object() -> None:
    function: Function = FunctionInferrer.infer_from_function_reference(add_location)
    assert function.parameters[0].type == JsonSchemaType.OBJECT.value


def test_infer_from_function_reference_with_primitive_list_parameter_returns_expected_type() -> (
    None
):
    function: Function = FunctionInferrer.infer_from_function_reference(add_locations)
    assert function.parameters[0].type == JsonSchemaType.ARRAY.value
    assert function.parameters[0].array_item_type == JsonSchemaType.OBJECT.value


def test_infer_from_function_reference_with_generic_primitive_list_parameter_raises_value_error() -> (
    None
):
    with pytest.raises(
        ValueError, match="Expected array parameter 'locations' to have an item type."
    ):
        FunctionInferrer.infer_from_function_reference(add_generic_locations)


def test_infer_from_function_reference_with_typing_list_parameter_raises_value_error() -> (
    None
):
    with pytest.raises(
        ValueError, match="Expected array parameter 'locations' to have an item type."
    ):
        FunctionInferrer.infer_from_function_reference(add_generic_typing_locations)


def test_infer_from_function_reference_adds_expected_required_parameters() -> None:
    function: Function = FunctionInferrer.infer_from_function_reference(
        get_temperature_with_default
    )

    assert function.required_parameters == ["location"]


def test_infer_from_function_reference_with_no_defaults_returns_required_parameters() -> (
    None
):
    function: Function = FunctionInferrer.infer_from_function_reference(get_temperature)

    assert set(function.required_parameters) == {"unit", "location"}


def test_infer_from_function_reference_with_all_defaults_returns_no_required_parameters() -> (
    None
):
    function: Function = FunctionInferrer.infer_from_function_reference(
        get_temperature_with_all_defaults
    )

    assert len(function.required_parameters) == 0


def test_infer_from_function_reference_with_optional_parameters_not_included_in_required() -> (
    None
):
    function: Function = FunctionInferrer.infer_from_function_reference(
        get_local_places_with_optional_location
    )
    assert function.required_parameters == []
