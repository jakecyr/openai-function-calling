"""Test the Parameter class."""

from openai_function_calling.parameter import Parameter, ParameterDict
import pytest


def test_to_dict_with_description_returns_dict_with_description() -> None:
    description = "Unit of temperature."
    unit_parameter = Parameter(
        name="unit",
        type="string",
        description=description,
        enum=["celsius", "fahrenheit"],
    )

    unit_parameter_dict: ParameterDict = unit_parameter.to_dict()

    assert unit_parameter_dict.get("description") == description


def test_to_dict_without_description_returns_dict_without_description_key() -> None:
    unit_parameter = Parameter(
        name="unit",
        type="string",
        enum=["celsius", "fahrenheit"],
    )

    unit_parameter_dict: ParameterDict = unit_parameter.to_dict()

    with pytest.raises(KeyError):
        unit_parameter_dict["description"]


def test_to_dict_with_enum_returns_dict_with_enum() -> None:
    enum: list[str] = ["celsius", "fahrenheit"]
    unit_parameter = Parameter(
        name="unit",
        type="string",
        enum=enum,
    )

    unit_parameter_dict: ParameterDict = unit_parameter.to_dict()

    assert unit_parameter_dict.get("enum") == enum


def test_to_dict_without_enum_returns_dict_without_enum_key() -> None:
    unit_parameter = Parameter(
        name="unit",
        type="string",
    )

    unit_parameter_dict: ParameterDict = unit_parameter.to_dict()

    with pytest.raises(KeyError):
        unit_parameter_dict["enum"]


def test_to_dict_returns_dict() -> None:
    unit_parameter = Parameter(
        name="unit",
        type="string",
    )

    unit_parameter_dict: ParameterDict = unit_parameter.to_dict()

    assert isinstance(unit_parameter_dict, dict)


def test_to_dict_returns_dict_with_expected_type() -> None:
    parameter_type = "string"

    unit_parameter = Parameter(
        name="unit",
        type=parameter_type,
    )

    unit_parameter_dict: ParameterDict = unit_parameter.to_dict()

    assert unit_parameter_dict["type"] == parameter_type
