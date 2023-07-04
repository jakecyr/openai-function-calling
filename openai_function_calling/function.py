"""Define the Function class and related objects."""


from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, TypedDict
from warnings import warn

from docstring_parser import Docstring, parser
from typing_extensions import NotRequired, deprecated

from openai_function_calling.helper_functions import python_type_to_json_schema_type
from openai_function_calling.json_schema_type import JsonSchemaType
from openai_function_calling.parameter import Parameter, ParameterDict

if TYPE_CHECKING:
    from collections.abc import Callable


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
    """A Python function wrapper that converts to JSON schema."""

    def __init__(
        self,
        name: str,
        description: str,
        parameters: list[Parameter] | None = None,
        required_parameters: list[str] | None = None,
    ) -> None:
        """Create a new function instance.

        Args:
            name: The name of the function.
            description: A description of the function's purpose.
            parameters: A list of parameters.
            required_parameters: A list of parameter names that are required to run the\
                function.
        """
        self.name: str = name
        self.description: str = description
        self.parameters: list[Parameter] = parameters or []
        self.required_parameters: list[str] | None = required_parameters

        self.validate()

    def validate(self) -> None:
        """Validate the function properties."""
        if not self.required_parameters:
            return

        parameter_names = {p.name for p in self.parameters or []}

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

        if self.required_parameters is None or len(self.required_parameters) == 0:
            return output_dict

        output_dict["parameters"]["required"] = self.required_parameters

        return output_dict

    @staticmethod
    def from_function(function_reference: Callable) -> Function:
        """Infer a function definition given a function reference.

        The type hints and docstring are used to infer the type and descriptions.

        Args:
            function_reference: The function reference to generate a definition for.

        Return:
            An instance of Function with inferred values.
        """
        function_description: str = ""
        parameters_by_name: dict[str, Parameter] = {}

        if hasattr(function_reference, "__doc__") and function_reference.__doc__:
            docstring: str = function_reference.__doc__
            parsed_docstring: Docstring = parser.parse(docstring)

            function_description = (
                parsed_docstring.short_description
                or parsed_docstring.long_description
                or ""
            )

            for param in parsed_docstring.params:
                parameters_by_name[param.arg_name] = Parameter(
                    name=param.arg_name,
                    type=python_type_to_json_schema_type(param.type_name),
                    description=param.description,
                )
        else:
            warn("Unable to find a docstring on the referenced function.", stacklevel=1)

        if hasattr(function_reference, "__annotations__"):
            annotations: dict[str, Any] = function_reference.__annotations__

            # If arguments are defined in the docstring and they don't match the count in the function defintion
            # throw an error
            if (
                len(parameters_by_name) > 0
                and len(annotations) != 1
                and len(parameters_by_name) != len(annotations) - 1
            ):
                raise ValueError(
                    "Mismatch between argument count in function definition "
                    "and function docstring.",
                )

            for key in annotations:
                if key == "return":
                    continue

                parameter_type: str = python_type_to_json_schema_type(
                    annotations[key].__name__,
                )

                if key not in parameters_by_name:
                    parameters_by_name[key] = Parameter(name=key, type=parameter_type)
                elif (
                    key in parameters_by_name
                    and parameters_by_name[key].type == JsonSchemaType.NULL
                ):
                    parameters_by_name[key].type = parameter_type

        inspected_parameters = inspect.signature(function_reference).parameters

        if len(parameters_by_name) > 0 and len(parameters_by_name) != len(
            inspected_parameters,
        ):
            raise RuntimeError(
                "The count of arguments found from the docstring and annotations "
                "does not match the actual function arguments.",
            )

        for name, parameter in inspected_parameters.items():
            parameter_type = python_type_to_json_schema_type(parameter.kind.name)

            if name not in parameters_by_name:
                parameters_by_name[name] = Parameter(name=name, type=parameter_type)
            elif (
                name in parameters_by_name
                and parameters_by_name[name].type == JsonSchemaType.NULL
            ):
                parameters_by_name[name].type = parameter_type

        parameters_list = list(parameters_by_name.values())

        return Function(
            name=function_reference.__name__,
            description=function_description,
            parameters=parameters_list,
        )
