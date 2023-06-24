from typing import Optional, TypedDict
from typing_extensions import NotRequired
from openai_function_calling.parameter import Parameter, ParameterDict


class ParametersDict(TypedDict):
    type: str
    properties: dict[str, ParameterDict]
    required: NotRequired[list[str]]


class FunctionDict(TypedDict):
    name: str
    description: str
    parameters: ParametersDict
    required: NotRequired[list[str]]


class Function:
    def __init__(
        self,
        name: str,
        description: str,
        parameters: Optional[list[Parameter]] = None,
        required_parameters: Optional[list[str]] = None,
    ) -> None:
        self.name: str = name
        self.description: str = description
        self.parameters: list[Parameter] | None = parameters
        self.required_parameters: list[str] | None = required_parameters

    def to_dict(self) -> FunctionDict:
        parameters_dict: dict[str, ParameterDict] = {}

        for parameter in self.parameters or []:
            parameters_dict[parameter.name] = parameter.to_dict()

        if self.required_parameters:
            parameters_dict["required"]

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": parameters_dict,
                "required": ["location"],
            },
        }
