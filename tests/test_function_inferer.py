"""Test the function inferer class."""

from openai_function_calling.function import Function
from openai_function_calling.function_inferer import FunctionInferer


def fully_documented_sum(a: int, b: int) -> int:
    """Sum two values.

    Args:
        a: The first value to sum.
        b: The second value to sum.

    Returns:
        The sum of the two values.
    """
    return a + b


def no_docstring_sum(a: int, b: int) -> int:
    return a + b


def test_infer_from_function_reference_returns_a_function_instance() -> None:
    function: Function = FunctionInferer.infer_from_function_reference(
        fully_documented_sum
    )

    assert isinstance(function, Function)


def test_infer_from_function_reference_returns_function_with_name_defined() -> None:
    function: Function = FunctionInferer.infer_from_function_reference(
        fully_documented_sum
    )

    assert function.name == fully_documented_sum.__name__


def test_infer_from_function_reference_returns_function_with_description_defined() -> (
    None
):
    function: Function = FunctionInferer.infer_from_function_reference(
        fully_documented_sum
    )

    assert function.description == "Sum two values."


def test_infer_from_function_reference_returns_function_with_expected_parameter_count() -> (
    None
):
    function: Function = FunctionInferer.infer_from_function_reference(
        fully_documented_sum
    )

    assert len(function.parameters) == 2


def test_infer_from_function_reference_returns_function_with_expected_parameter_attributes() -> (
    None
):
    function: Function = FunctionInferer.infer_from_function_reference(
        fully_documented_sum
    )

    assert function.parameters[0].name == "a"
    assert function.parameters[0].type == "integer"
    assert function.parameters[0].description == "The first value to sum."
    assert function.parameters[0].array_item_type is None
    assert function.parameters[0].enum is None

    assert function.parameters[1].name == "b"
    assert function.parameters[1].type == "integer"
    assert function.parameters[1].description == "The second value to sum."
    assert function.parameters[1].array_item_type is None
    assert function.parameters[1].enum is None


def test_infer_from_function_reference_returns_function_with_expected_values() -> None:
    function: Function = FunctionInferer.infer_from_function_reference(no_docstring_sum)

    assert function.name == no_docstring_sum.__name__
    assert len(function.parameters) == 2
    assert function.parameters[0].name == "a"
    assert function.parameters[0].type == "integer"
    assert function.parameters[1].name == "b"
    assert function.parameters[1].type == "integer"
