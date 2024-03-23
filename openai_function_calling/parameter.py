"""Define the Parameter class and related objects."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypedDict

from openai_function_calling.json_schema_type import JsonSchemaType

if TYPE_CHECKING:  # pragma: no cover
    from typing_extensions import NotRequired


class ItemsDict(TypedDict):
    """JSON Schema representation of array items."""

    type: str


class ParameterDict(TypedDict):
    """JSON Schema representation of a parameter."""

    type: str
    description: NotRequired[str]
    enum: NotRequired[list[Any]]
    items: NotRequired[ItemsDict]


class Parameter:
    """A wrapper for function parameters to convert them to JSON schema."""

    def __init__(
        self,
        name: str,
        type: JsonSchemaType | str,
        description: str | None = None,
        *,
        enum: list[Any] | None = None,
        array_item_type: str | None = None,
    ) -> None:
        """Create a new parameter instance.

        Args:
            name: The name of the parameter as defined in the function.
            type: The JSON schema type of the parameter.
            description: A description of the parameter.
            enum: A list of allowed values for the parameter.
            array_item_type: If the type is set to 'array', the JSON\
                schema type of the items it contains.

        Raises:
            ValueError: If the 'type' is set to 'array', but 'array_item_type' argument\
                is not set.
            ValueError: If the 'array_item_type' argument is set, but the 'type' is not\
                'array'.

        """
        self.name: str = name
        self.type: str = type
        self.description: str | None = description
        self.enum: list[Any] | None = enum
        self.array_item_type: str | None = array_item_type

        self.validate()

    def validate(self) -> None:
        """Validate the parameter has valid properties.

        Raises:
            ValueError: If 'array_item_type' is not set, but 'type' is array.
            ValueError: If 'array_item_type' is set, but 'type' is not array.

        """
        if self.type == JsonSchemaType.ARRAY and self.array_item_type is None:
            raise ValueError(
                "Expected 'array_item_type' value since type is set to 'array'.",
            )

        if self.type != JsonSchemaType.ARRAY and self.array_item_type is not None:
            raise ValueError(
                "Unexpected 'array_item_type' value since type is not set to 'array'.",
            )

    def to_json_schema(self) -> ParameterDict:
        """Convert to a JSON schema dict object.

        Returns:
            A dict representation of the parameter in a JSON schema format.

        Raises:
            ValueError: If there are validation errors. See the validate method.

        """
        self.validate()

        output_dict: ParameterDict = {
            "type": self.type,
        }

        if self.description:
            output_dict["description"] = self.description

        if self.enum:
            output_dict["enum"] = self.enum

        if self.array_item_type:
            output_dict["items"] = {"type": self.array_item_type}

        return output_dict

    def merge(self, other_parameter: Parameter) -> None:
        """Merge another parameter into the current instance.

        Will not replace values that already exist.

        Args:
            other_parameter: The other parameter instance to merge into the current.

        """
        if not isinstance(other_parameter, Parameter):
            raise TypeError("Cannot merge non-parameter type into parameter.")

        if self.name is None:
            self.name = other_parameter.name

        if self.type is None or self.type == JsonSchemaType.NULL:
            self.type = other_parameter.type

        if self.description is None:
            self.description = other_parameter.description

        if self.enum is None:
            self.enum = other_parameter.enum

        if self.array_item_type is None or self.array_item_type == JsonSchemaType.NULL:
            self.array_item_type = other_parameter.array_item_type

    def __eq__(self, other: object) -> bool:
        """Test if an object is equivalent to the parameter.

        Args:
            other: The other value to compare against.

        Returns:
            If the other object is equal to the current instance.

        """
        if not isinstance(other, Parameter):
            return False

        return (
            self.name == other.name
            and self.type == other.type
            and self.description == other.description
            and self.enum == other.enum
            and self.array_item_type == other.array_item_type
        )
