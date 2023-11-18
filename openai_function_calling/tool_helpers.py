"""Class to help with converting function definitions to tool parameters."""

from __future__ import annotations

from typing import Callable, cast
from openai.types.chat import ChatCompletionToolParam
from openai.types.shared_params import FunctionDefinition
from openai_function_calling.function import Function, FunctionDict
from openai_function_calling.function_inferrer import FunctionInferrer


class ToolHelpers:
    @staticmethod
    def from_functions(functions: list[Function]) -> list[ChatCompletionToolParam]:
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
        functions: list[Function] = [
            FunctionInferrer.infer_from_function_reference(f) for f in function_refs
        ]
        return ToolHelpers.from_functions(functions)

    @staticmethod
    def json_schema_to_tool_param(json_schema: FunctionDict) -> ChatCompletionToolParam:
        return {"type": "function", "function": cast(FunctionDefinition, json_schema)}
