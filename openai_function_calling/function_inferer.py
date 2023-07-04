from typing import Callable
from warnings import warn

from docstring_parser import Docstring, parser

from openai_function_calling.function import Function
from openai_function_calling.helper_functions import python_type_to_json_schema_type
from openai_function_calling.parameter import Parameter


class FunctionInferer:
    @staticmethod
    def infer_from_docstring(function_reference: Callable) -> Function:
        function_definition = Function(
            name=function_reference.__name__, description="", parameters=[]
        )
        parameters_by_name: dict[str, Parameter] = {}

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
            parameters_by_name[param.arg_name] = Parameter(
                name=param.arg_name,
                type=python_type_to_json_schema_type(param.type_name),
                description=param.description,
            )

        return function_definition
