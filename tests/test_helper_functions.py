"""Helper function tests."""


import pytest

from openai_function_calling.helper_functions import python_type_to_json_schema_type
from openai_function_calling.json_schema_type import JsonSchemaType


def test_null():
    assert python_type_to_json_schema_type(None) == JsonSchemaType.NULL.value


@pytest.mark.parametrize("json_schema_type", list(JsonSchemaType))
def test_json_schema_type_values(json_schema_type) -> None:
    assert (
        python_type_to_json_schema_type(json_schema_type.value)
        == json_schema_type.value
    )


def test_int() -> None:
    assert python_type_to_json_schema_type("int") == JsonSchemaType.INTEGER.value


def test_float() -> None:
    assert python_type_to_json_schema_type("float") == JsonSchemaType.NUMBER.value


def test_complex() -> None:
    assert python_type_to_json_schema_type("complex") == JsonSchemaType.NUMBER.value


def test_str() -> None:
    assert python_type_to_json_schema_type("str") == JsonSchemaType.STRING.value


def test_bool() -> None:
    assert python_type_to_json_schema_type("bool") == JsonSchemaType.BOOLEAN.value


def test_dict() -> None:
    assert python_type_to_json_schema_type("dict") == JsonSchemaType.OBJECT.value


def test_list() -> None:
    assert python_type_to_json_schema_type("list") == JsonSchemaType.ARRAY.value
