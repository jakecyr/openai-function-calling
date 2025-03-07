"""Function inferrer class definition."""

from __future__ import annotations

import dataclasses
import inspect
import typing
from enum import EnumMeta
from typing import TYPE_CHECKING, Any, get_args, get_origin, get_type_hints
from warnings import warn

from docstring_parser import Docstring, parser

from openai_function_calling.function import Function
from openai_function_calling.helper_functions import python_type_to_json_schema_type
from openai_function_calling.json_schema_type import JsonSchemaType
from openai_function_calling.parameter import Parameter

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable


class FunctionInferrer:
    """Class to help inferring a function definition from a reference."""

    @staticmethod
    def infer_from_function_reference(function_reference: Callable) -> Function:
        """Infer a function definition given a function reference.

        The type hints and docstring are used to infer the type and descriptions.

        Args:
            function_reference: The function reference to generate a definition for.

        Return:
            An instance of Function with inferred values.

        """
        inferred_from_annotations: Function = FunctionInferrer._infer_from_annotations(
            function_reference
        )
        inferred_from_docstring: Function = FunctionInferrer._infer_from_docstring(
            function_reference
        )
        inferred_from_inspection: Function = FunctionInferrer._infer_from_inspection(
            function_reference
        )

        inferred_from_annotations.merge(inferred_from_docstring)
        inferred_from_annotations.merge(inferred_from_inspection)

        return inferred_from_annotations

    @staticmethod
    def _infer_from_docstring(function_reference: Callable) -> Function:
        """Infer a function definition from a docstring.

        Args:
            function_reference: The function reference to use for inference.

        Returns:
            The inferred Function instance.

        """
        function_definition = Function(
            name=function_reference.__name__,
            description="",
            parameters=[],
        )

        if not hasattr(function_reference, "__doc__") or not function_reference.__doc__:
            warn("Unable to find a docstring on the referenced function.", stacklevel=1)
            return function_definition

        docstring: str = function_reference.__doc__
        parsed_docstring: Docstring = parser.parse(docstring)

        function_definition.description = (
            parsed_docstring.short_description
            or parsed_docstring.long_description
            or ""
        )

        for param in parsed_docstring.params:
            function_definition.parameters.append(
                Parameter(
                    name=param.arg_name,
                    type=python_type_to_json_schema_type(param.type_name),
                    description=param.description,
                )
            )

        return function_definition

    @staticmethod
    def _infer_from_annotations(function_reference: Callable) -> Function:
        """Infer a function definition from annotations.

        Args:
            function_reference: The function reference to use for inference.

        Returns:
            The inferred Function instance.

        """
        annotations: dict[str, Any] = get_type_hints(function_reference)
        parameters: list[Parameter] = []

        for param_name, annotation_type in annotations.items():
            if param_name == "return":
                continue

            origin = get_origin(annotation_type) or annotation_type
            args: tuple[Any, ...] = get_args(annotation_type)

            if origin in [list, typing.List]:  # noqa: UP006
                if not args:
                    raise ValueError(
                        f"Expected array parameter '{param_name}' to have an item type."
                    )
                item_type = args[0]
                parameter_type = JsonSchemaType.ARRAY.value
                array_item_type = python_type_to_json_schema_type(
                    item_type.__name__ if hasattr(item_type, "__name__") else "Any"
                )
            elif origin in [dict, typing.Dict]:  # noqa: UP006
                parameter_type = JsonSchemaType.OBJECT.value
                array_item_type = None
            else:
                parameter_type = python_type_to_json_schema_type(
                    annotation_type.__name__
                    if hasattr(annotation_type, "__name__")
                    else "Any"
                )

                array_item_type = None

            parameters.append(
                Parameter(
                    name=param_name,
                    type=parameter_type,
                    array_item_type=array_item_type,
                )
            )

        return Function(
            name=function_reference.__name__,
            description="",
            parameters=parameters,
        )

    @staticmethod
    def _infer_from_inspection(function_reference: Callable) -> Function:
        """Infer a function definition by inspecting the signature.

        Args:
            function_reference: The function reference to use for inference.

        Returns:
            The inferred Function instance.

        """
        function_definition = Function(
            name=function_reference.__name__,
            description="",
            parameters=[],
        )
        inspected_signature: inspect.Signature = inspect.signature(function_reference)
        inspected_parameters = inspected_signature.parameters

        for name, parameter in inspected_parameters.items():
            parameter_type: str = python_type_to_json_schema_type(parameter.kind.name)
            enum_values: list[str] | None = None

            if parameter.default is inspect.Parameter.empty:
                function_definition.required_parameters.append(name)

            if parameter_type == "null":
                if isinstance(parameter.annotation, EnumMeta):
                    enum_values = list(parameter.annotation._value2member_map_.keys())
                    parameter_type = FunctionInferrer._infer_list_item_type(enum_values)
                elif dataclasses.is_dataclass(parameter.annotation):
                    parameter_type = JsonSchemaType.OBJECT.value

            function_definition.parameters.append(
                Parameter(name=name, type=parameter_type, enum=enum_values)
            )

        return function_definition

    @staticmethod
    def _infer_list_item_type(list_of_items: list[Any]) -> str:
        if len(list_of_items) == 0:
            return JsonSchemaType.NULL.value

        # Check if all items are the same type.
        if len({type(item).__name__ for item in list_of_items}) == 1:
            item: Any = type(list_of_items[0]).__name__
            return python_type_to_json_schema_type(item)

        return JsonSchemaType.ANY.value
