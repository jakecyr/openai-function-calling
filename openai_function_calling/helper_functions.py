"""Helper functions used throughout the package."""

from __future__ import annotations

from openai_function_calling.json_schema_type import JsonSchemaType


def python_type_to_json_schema_type(python_type: str | None) -> str:
    """Convert a python type string to a value JSON schema type.

    Args:
        python_type: A string representation of a python type.

    Returns:
        A JSON schema type value.

    """
    json_schema_type: str = JsonSchemaType.NULL.value

    if python_type in {f.value for f in JsonSchemaType}:
        json_schema_type = python_type

    if python_type == "int":
        json_schema_type = JsonSchemaType.INTEGER.value

    if python_type in {"float", "complex"}:
        json_schema_type = JsonSchemaType.NUMBER.value

    if python_type == "str":
        json_schema_type = JsonSchemaType.STRING.value

    if python_type == "bool":
        json_schema_type = JsonSchemaType.BOOLEAN.value

    if python_type == "dict":
        json_schema_type = JsonSchemaType.OBJECT.value

    if python_type == "list":
        json_schema_type = JsonSchemaType.ARRAY.value

    return json_schema_type
