"""Define the Function class and related objects."""

from typing import Optional, TypedDict
from typing_extensions import NotRequired
from openai_function_calling.json_schema_type import JsonSchemaType
from openai_function_calling.parameter import Parameter, ParameterDict


class ParametersDict(TypedDict):
    """A JSON schema representation of a parameter object."""

    type: str
    properties: dict[str, ParameterDict]
    required: NotRequired[list[str]]


class FunctionDict(TypedDict):
    """A JSON schema representation of a function."""

    name: str
    description: str
    parameters: ParametersDict


class Function:
    """A wrapper for an existing Python function that automatically converts
    to JSON schema."""

    def __init__(
        self,
        name: str,
        description: str,
        parameters: Optional[list[Parameter]] = None,
        required_parameters: Optional[list[str]] = None,
    ) -> None:
        """Create a new function instance.

        Args:
            name: The name of the function.
            description: A description of the function's purpose.
            parameters: A list of parameters.
            required_parameter: A list of parameter names that are required to run the\
                function.
        """
        self.name: str = name
        self.description: str = description
        self.parameters: list[Parameter] | None = parameters
        self.required_parameters: list[str] | None = required_parameters

        self.validate()

    def validate(self) -> None:
        """Validate the function properties."""
        if not self.required_parameters:
            return

        parameter_names = set(p.name for p in self.parameters or [])

        for required_parameter in self.required_parameters:
            if required_parameter not in parameter_names:
                raise ValueError(
                    f"Cannot require a parameter, '{required_parameter}', that is not "
                    "defined."
                )

    def to_json_schema(self) -> FunctionDict:
        """Convert the function instance to a JSON schema dict.

        Raises:
            ValueError: If a parameter is marked as required, but it not defined.

        Returns:
            A JSON schema representation of the function.
        """
        self.validate()

        parameters_dict: dict[str, ParameterDict] = {
            p.name: p.to_json_schema() for p in self.parameters or []
        }

        output_dict: FunctionDict = {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": JsonSchemaType.OBJECT,
                "properties": parameters_dict,
            },
        }

        if self.required_parameters is None or len(self.required_parameters) == 0:
            return output_dict

        output_dict["parameters"]["required"] = self.required_parameters

        return output_dict
