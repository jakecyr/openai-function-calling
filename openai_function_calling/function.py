"""Define the Function class and related objects."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from typing_extensions import NotRequired, deprecated  # type: ignore[attr-defined]

from openai_function_calling.json_schema_type import JsonSchemaType

if TYPE_CHECKING:  # pragma: no cover
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
    strict: NotRequired[bool]


class Function:
    """A Python function wrapper that converts to JSON schema."""

    def __init__(
        self,
        name: str,
        description: str,
        parameters: list[Parameter] | None = None,
        required_parameters: list[str] | None = None,
        strict: bool | None = None,
    ) -> None:
        """Create a new function instance.

        Args:
            name: The name of the function.
            description: A description of the function's purpose.
            parameters: A list of parameters.
            required_parameters: A list of parameter names that are required to run the\
                function.
            strict: If the function should enforce strict parameters.

        """
        self.name: str = name
        self.description: str = description
        self.parameters: list[Parameter] = parameters or []
        self.required_parameters: list[str] = required_parameters or []
        self.strict: bool | None = strict

        self.validate()

    def validate(self) -> None:
        """Validate the function properties."""
        if not self.required_parameters:
            return

        parameter_names: set[str] = {p.name for p in self.parameters or []}

        for required_parameter in self.required_parameters:
            if required_parameter not in parameter_names:
                raise ValueError(
                    f"Cannot require a parameter, '{required_parameter}', that is not "
                    "defined.",
                )

    @deprecated(
        "The to_dict method has been deprecated in favor of the "
        "to_json_schema method. Please use the to_json_schema method instead.",
    )
    def to_dict(self) -> FunctionDict:
        """Convert the function instance to a JSON schema dict.

        Raises:
            ValueError: If a parameter is marked as required, but it not defined.

        Returns:
            A JSON schema representation of the function.

        """
        return self.to_json_schema()

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
                "type": JsonSchemaType.OBJECT.value,
                "properties": parameters_dict,
            },
        }

        if self.strict is not None:
            output_dict["strict"] = self.strict

        if self.required_parameters is None or len(self.required_parameters) == 0:
            return output_dict

        output_dict["parameters"]["required"] = self.required_parameters

        return output_dict

    def merge(self, other_function: Function) -> None:
        """Merge another function object into the current.

        Args:
            other_function: The other function to merge into the current.

        """
        if not self.name:
            self.name = other_function.name

        if not self.description:
            self.description = other_function.description

        self._merge_parameters(other_parameters=other_function.parameters)
        self._merge_required_parameters(
            other_required_parameters=other_function.required_parameters
        )

    def _merge_required_parameters(self, other_required_parameters: list[str]) -> None:
        if len(other_required_parameters) == 0:
            return

        if other_required_parameters == self.required_parameters:
            return

        required_parameters_set = set(self.required_parameters)
        other_required_parameters_set = set(other_required_parameters)

        self.required_parameters = list(
            required_parameters_set.union(other_required_parameters_set)
        )

    def _merge_parameters(self, other_parameters: list[Parameter]) -> None:
        if len(other_parameters) == 0:
            return

        current_parameters: dict[str, Parameter] = {f.name: f for f in self.parameters}

        for other_parameter in other_parameters:
            parameter_name: str = other_parameter.name

            if parameter_name in current_parameters:
                if other_parameter != current_parameters[parameter_name]:
                    current_parameters[parameter_name].merge(other_parameter)
            else:
                self.parameters.append(other_parameter)
