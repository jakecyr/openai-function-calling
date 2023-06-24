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

        output_dict: FunctionDict = {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": parameters_dict,
            },
        }

        if self.required_parameters is None or len(self.required_parameters) == 0:
            return output_dict

        for parameter in self.required_parameters:
            if parameter not in parameters_dict:
                raise ValueError(
                    "Cannot require a parameter that does not have a "
                    f"definition: '{parameter}'"
                )

        output_dict["parameters"]["required"] = self.required_parameters

        return output_dict
