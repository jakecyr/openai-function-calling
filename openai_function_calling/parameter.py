from typing import TypedDict, Optional, Any
from typing_extensions import NotRequired


class ParameterDict(TypedDict):
    type: str
    description: NotRequired[str]
    enum: NotRequired[list[Any]]


class Parameter:
    def __init__(
        self,
        name: str,
        type: str,
        description: Optional[str] = None,
        enum: Optional[list[Any]] = None,
    ) -> None:
        self.name: str = name
        self.type: str = type
        self.description: str | None = description
        self.enum: list[Any] | None = enum

    def to_dict(self) -> ParameterDict:
        output_dict: ParameterDict = {
            "type": self.type,
        }

        if self.description:
            output_dict["description"] = self.description

        if self.enum:
            output_dict["enum"] = self.enum

        return output_dict
