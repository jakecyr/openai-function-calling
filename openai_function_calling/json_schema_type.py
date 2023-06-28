"""Define an enumeration of JSON schema types."""

from enum import Enum


class JsonSchemaType(str, Enum):
    """An enumeration of JSON Schema type values."""

    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    OBJECT = "object"
    ARRAY = "array"
    NULL = "null"
    ANY = "any"
