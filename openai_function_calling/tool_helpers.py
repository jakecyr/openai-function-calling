"""Class to help with converting function definitions to tool parameters."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, cast

from openai.types.shared_params import FunctionDefinition

from openai_function_calling.function_inferrer import FunctionInferrer

if TYPE_CHECKING:  # pragma: no cover
    from openai.types.chat import ChatCompletionToolParam

    from openai_function_calling.function import Function, FunctionDict


class ToolHelpers:
    """Class to help with conversions from functions to tool parameters."""

    @staticmethod
    def from_functions(functions: list[Function]) -> list[ChatCompletionToolParam]:
        """Create OpenAI chat completion tool params from function definition objects.

        Args:
            functions: A list of function definition objects.

        Returns:
            A list of OpenAI chat completion tool parameters.

        """
        json_schemas: list[FunctionDict] = [f.to_json_schema() for f in functions]
        tool_params: list[ChatCompletionToolParam] = [
            ToolHelpers.json_schema_to_tool_param(json_schema)
            for json_schema in json_schemas
        ]
        return tool_params

    @staticmethod
    def infer_from_function_refs(
        function_refs: list[Callable],
    ) -> list[ChatCompletionToolParam]:
        """Create OpenAI chat completion tool parameters from function references.

        Args:
            function_refs: A list of function references.

        Returns:
            A list of OpenAI chat completion tool parameters.

        """
        functions: list[Function] = [
            FunctionInferrer.infer_from_function_reference(f) for f in function_refs
        ]
        return ToolHelpers.from_functions(functions)

    @staticmethod
    def json_schema_to_tool_param(json_schema: FunctionDict) -> ChatCompletionToolParam:
        """Convert a JSON schema object to an OpenAI chat completion tool parameter.

        Args:
            json_schema: A JSON schema object.

        Returns:
            An OpenAI chat completion tool parameter.

        """
        return {"type": "function", "function": cast(FunctionDefinition, json_schema)}
