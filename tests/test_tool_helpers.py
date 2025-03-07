"""Test the tool wrapper class."""

from typing import TYPE_CHECKING

from openai_function_calling.function import Function
from openai_function_calling.function_inferrer import FunctionInferrer
from openai_function_calling.tool_helpers import ToolHelpers

if TYPE_CHECKING:
    from openai.types.chat import ChatCompletionToolParam


def get_current_weather(location: str, unit: str) -> str:
    """Get the current weather and return a summary."""
    return f"It is currently sunny in {location} and 75 degrees {unit}."


get_current_weather_schema: Function = FunctionInferrer.infer_from_function_reference(
    get_current_weather,
)


def test_from_functions_returns_list() -> None:
    assert isinstance(ToolHelpers.from_functions([]), list)


def test_from_functions_returns_list_of_dicts() -> None:
    assert isinstance(
        ToolHelpers.from_functions([get_current_weather_schema])[0],
        dict,
    )


def test_from_functions_dicts_contain_expected_keys() -> None:
    tool_param: ChatCompletionToolParam = ToolHelpers.from_functions(
        [get_current_weather_schema]
    )[0]

    assert "type" in tool_param
    assert "function" in tool_param


def test_from_functions_dicts_function_is_dict() -> None:
    tool_param: ChatCompletionToolParam = ToolHelpers.from_functions(
        [get_current_weather_schema]
    )[0]

    assert isinstance(tool_param["function"], dict)


def test_from_functions_dicts_type_is_set_to_function() -> None:
    tool_param: ChatCompletionToolParam = ToolHelpers.from_functions(
        [get_current_weather_schema]
    )[0]

    assert tool_param["type"] == "function"


def test_from_functions_dicts_function_has_expected_keys() -> None:
    tool_param: ChatCompletionToolParam = ToolHelpers.from_functions(
        [get_current_weather_schema]
    )[0]

    assert "name" in tool_param["function"]
    assert "description" in tool_param["function"]
    assert "parameters" in tool_param["function"]


def test_from_functions_dicts_function_parameters_has_expected_type() -> None:
    tool_param: ChatCompletionToolParam = ToolHelpers.from_functions(
        [get_current_weather_schema]
    )[0]

    assert "parameters" in tool_param["function"]
    assert isinstance(tool_param["function"]["parameters"], dict)


def test_infer_from_function_refs_returns_list() -> None:
    assert isinstance(ToolHelpers.infer_from_function_refs([get_current_weather]), list)


def test_infer_from_function_refs_returns_list_of_dicts() -> None:
    assert isinstance(
        ToolHelpers.infer_from_function_refs([get_current_weather])[0],
        dict,
    )


def test_infer_from_function_refs_dicts_contain_expected_keys() -> None:
    tool_param: ChatCompletionToolParam = ToolHelpers.infer_from_function_refs(
        [get_current_weather]
    )[0]

    assert "type" in tool_param
    assert "function" in tool_param


def test_infer_from_function_refs_dicts_function_is_dict() -> None:
    tool_param: ChatCompletionToolParam = ToolHelpers.infer_from_function_refs(
        [get_current_weather]
    )[0]

    assert isinstance(tool_param["function"], dict)
