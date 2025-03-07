"""Test the Parameter class."""

import pytest

from openai_function_calling.json_schema_type import JsonSchemaType
from openai_function_calling.parameter import Parameter, ParameterDict


def test_to_json_schema_with_description_returns_dict_with_description() -> None:
    description = "Unit of temperature."
    unit_parameter = Parameter(
        name="unit",
        type=JsonSchemaType.STRING,
        description=description,
        enum=["celsius", "fahrenheit"],
    )

    unit_parameter_dict: ParameterDict = unit_parameter.to_json_schema()

    assert unit_parameter_dict.get("description") == description


def test_to_json_schema_without_description_returns_dict_without_description_key() -> (
    None
):
    unit_parameter = Parameter(
        name="unit",
        type=JsonSchemaType.STRING,
        enum=["celsius", "fahrenheit"],
    )

    unit_parameter_dict: ParameterDict = unit_parameter.to_json_schema()

    with pytest.raises(KeyError):
        unit_parameter_dict["description"]


def test_to_json_schema_with_enum_returns_dict_with_enum() -> None:
    enum: list[str] = ["celsius", "fahrenheit"]
    unit_parameter = Parameter(
        name="unit",
        type=JsonSchemaType.STRING,
        enum=enum,
    )

    unit_parameter_dict: ParameterDict = unit_parameter.to_json_schema()

    assert unit_parameter_dict.get("enum") == enum


def test_to_json_schema_without_enum_returns_dict_without_enum_key() -> None:
    unit_parameter = Parameter(
        name="unit",
        type=JsonSchemaType.STRING,
    )

    unit_parameter_dict: ParameterDict = unit_parameter.to_json_schema()

    with pytest.raises(KeyError):
        unit_parameter_dict["enum"]


def test_to_json_schema_returns_dict() -> None:
    unit_parameter = Parameter(
        name="unit",
        type=JsonSchemaType.STRING,
    )

    unit_parameter_dict: ParameterDict = unit_parameter.to_json_schema()

    assert isinstance(unit_parameter_dict, dict)


def test_to_json_schema_returns_dict_with_expected_type() -> None:
    parameter_type: JsonSchemaType = JsonSchemaType.STRING

    unit_parameter = Parameter(
        name="unit",
        type=parameter_type,
    )

    unit_parameter_dict: ParameterDict = unit_parameter.to_json_schema()

    assert unit_parameter_dict["type"] == parameter_type


def test_init_with_type_array_and_no_array_item_type_raises_value_error() -> None:
    with pytest.raises(
        ValueError,
        match="Expected 'array_item_type' value since type is set to 'array'*",
    ):
        Parameter(
            name="unit",
            type=JsonSchemaType.ARRAY,
        )


def test_init_with_type_not_array_with_array_item_type_raises_value_error() -> None:
    with pytest.raises(
        ValueError,
        match="Unexpected 'array_item_type' value since type is not set to 'array'*",
    ):
        Parameter(
            name="unit",
            type=JsonSchemaType.STRING,
            array_item_type=JsonSchemaType.STRING,
        )


def test_to_json_schema_with_type_array_items_returns_expected_dict() -> None:
    parameter = Parameter(
        name="unit",
        type=JsonSchemaType.ARRAY,
        array_item_type=JsonSchemaType.STRING,
    )

    parameter_dict: ParameterDict = parameter.to_json_schema()

    assert "items" in parameter_dict, (
        "Expected parameter dict to have 'items' property."
    )
    assert "type" in parameter_dict["items"], (
        "Expected parameter 'items' dict to have 'type' property."
    )
    assert isinstance(parameter_dict["items"]["type"], str)
    assert parameter_dict["items"]["type"] == JsonSchemaType.STRING


def test_eq_returns_true_if_parameters_are_equal() -> None:
    parameter = Parameter(
        name="unit",
        type=JsonSchemaType.ARRAY,
        array_item_type=JsonSchemaType.STRING,
    )
    other_parameter = Parameter(
        name="unit",
        type=JsonSchemaType.ARRAY,
        array_item_type=JsonSchemaType.STRING,
    )

    assert parameter == other_parameter


def test_eq_returns_false_if_parameters_are_not_equal() -> None:
    parameter = Parameter(
        name="unit",
        type=JsonSchemaType.ARRAY,
        array_item_type=JsonSchemaType.STRING,
    )
    other_parameter = Parameter(
        name="other",
        type=JsonSchemaType.ARRAY,
        array_item_type=JsonSchemaType.STRING,
    )

    assert parameter != other_parameter


def test_merge_replaces_values_if_they_are_not_defined() -> None:
    parameter = Parameter(
        name="unit",
        type=JsonSchemaType.NULL,
    )
    other_parameter = Parameter(
        name="other",
        type=JsonSchemaType.ARRAY,
        array_item_type=JsonSchemaType.STRING,
        description="Some description",
    )

    parameter.merge(other_parameter)

    assert parameter.type == JsonSchemaType.ARRAY
    assert parameter.array_item_type == JsonSchemaType.STRING
    assert parameter.description == "Some description"


def test_merge_does_not_remove_values() -> None:
    parameter = Parameter(
        name="other",
        type=JsonSchemaType.ARRAY,
        array_item_type=JsonSchemaType.STRING,
        description="Some description",
    )
    other_parameter = Parameter(
        name="unit",
        type=JsonSchemaType.NULL,
    )

    parameter.merge(other_parameter)

    assert parameter.type == JsonSchemaType.ARRAY
    assert parameter.array_item_type == JsonSchemaType.STRING
    assert parameter.description == "Some description"


def test_merge_with_invalid_type_raises_type_error() -> None:
    parameter = Parameter(
        name="unit",
        type=JsonSchemaType.NULL,
    )

    with pytest.raises(TypeError):
        parameter.merge(1)  # type: ignore
