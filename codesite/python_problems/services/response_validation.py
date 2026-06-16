import json
from collections import Counter
from python_problems.models import ComparisonType
from .problem_test_case_parsing import get_field
from .ui_problem_test_cases import (
    get_problem_metadata,
)
from .validators import (
    validate_find_unique_binary_string
)

VALIDATORS = {
    # slug: function name
    "find-unique-binary-string": validate_find_unique_binary_string,
}


def freeze(value):
    if isinstance(value, list):
        return tuple(freeze(item) for item in value)

    if isinstance(value, dict):
        return tuple(sorted(
            (key, freeze(val))
            for key, val in value.items()
        ))

    return value


def compare_output_and_expected(
        output_value_list,
        input_list,
        expected_list,
        comparison_type,
        language,
        problem_slug,
) -> bool:
    if len(output_value_list) != len(expected_list):
        return False

    for output_value, expected_value, input_data in zip(output_value_list, expected_list, input_list):
        match comparison_type:
            case ComparisonType.EXACT | "equal" | "exact":
                if output_value != expected_value:
                    return False

            case ComparisonType.UNORDERED:
                if (
                    type(output_value) != type(expected_value)
                    or len(output_value) != len(expected_value)
                    or {freeze(x) for x in output_value} != {freeze(x) for x in expected_value}
                ):
                    return False

            case ComparisonType.MULTISET:
                if (
                    type(output_value) != type(expected_value)
                    or len(output_value) != len(expected_value)
                    or Counter(freeze(x) for x in output_value) != Counter(freeze(x) for x in expected_value)
                ):
                    return False

            case ComparisonType.VALIDATOR:
                validator = VALIDATORS[problem_slug]
                if not validator(output_value, input_data):
                    return False

    return True


def validate_response(
    response,
    problem,
    language,
    button_pressed,
):
    if button_pressed != "validate":
        return

    input_list = []
    expected_list = []
    problem_test_cases = problem.get_shared_testcases(
        include_hidden=True) or None

    if not problem_test_cases:
        raise ValueError("No problem test cases found.")

    for problem_test_case in problem_test_cases:
        inputs = get_field(problem_test_case.data, "inputs")
        input_list.append(inputs)
        expected = get_field(problem_test_case.data, "expected")
        expected_list.append(expected)

    N = len(problem_test_cases)
    stdout = response.pop("stdout")
    output_serialized_list = stdout.strip().splitlines()[-N:]
    metadata = get_problem_metadata(problem)
    comparison_type = metadata.get("comparison_type", problem.comparison_type)

    output_value_list = [
        json.loads(line)
        for line in output_serialized_list
    ]

    if compare_output_and_expected(
        output_value_list,
        input_list,
        expected_list,
        comparison_type,
        language,
        problem.slug,
    ):
        response["result"] = "Tests passed!"
    else:
        response["result"] = "Tests failed!"

    return
