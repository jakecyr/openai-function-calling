from typing import TypedDict, Optional, Any
from typing_extensions import NotRequired


class ItemsDict(TypedDict):
    type: str


class ParameterDict(TypedDict):
    type: str
    description: NotRequired[str]
    enum: NotRequired[list[Any]]
    items: NotRequired[ItemsDict]


class Parameter:
    def __init__(
        self,
        name: str,
        type: str,
        description: Optional[str] = None,
        *,
        enum: Optional[list[Any]] = None,
        array_item_type: Optional[str] = None,
    ) -> None:
        """Create a new parameter instance.

        Args:
            name: The name of the parameter as defined in the function.
            type: The JSON schema type of the parameter.
            description: A description of the parameter.
            enum: A list of allowed values for the parameter.
            array_item_type: If the type is set to 'array', the JSON\
                schema type of the items it contains.
        """
        if type == "array" and array_item_type is None:
            raise ValueError(
                "Expected 'array_item_type' value since type is set to 'array'."
            )

        if type != "array" and array_item_type is not None:
            raise ValueError(
                "Unexpected 'array_item_type' value since type is not set to 'array'."
            )

        self.name: str = name
        self.type: str = type
        self.description: str | None = description
        self.enum: list[Any] | None = enum
        self.array_item_type: str | None = array_item_type

    def to_dict(self) -> ParameterDict:
        """Convert to a JSON schema dict object.

        Returns:
            A dict representation of the parameter in a JSON schema format.
        """
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
