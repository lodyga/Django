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
        return tuple(sorted((
            key, freeze(val))
            for key, val in value.items()
        ))

    return value


def compare_output_and_expected(
        input_list,
        output_value_list,
        expected_list,
        comparison_type,
        problem_slug) -> bool:

    if len(output_value_list) != len(expected_list) != len(input_list):
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


def get_output_list(response, test_case_size):
    test_case_size = len(test_case_size)
    stdout = response.pop("stdout")
    output_serialized_list = stdout.strip().splitlines()[-test_case_size:]

    return [json.loads(line)
            for line in output_serialized_list
            ]


def validate_response(response, problem, button_pressed) -> None:
    if button_pressed != "validate":
        return

    metadata = problem.metadata
    problem_test_cases = problem.get_shared_testcases(
        include_hidden=True
    )
    input_list = [
        get_field(problem_test_case.data, "inputs")
        for problem_test_case in problem_test_cases
    ]
    expected_list = [
        get_field(problem_test_case.data, "expected")
        for problem_test_case in problem_test_cases
    ]
    output_list = get_output_list(response, problem_test_cases)

    if compare_output_and_expected(
            input_list,
            output_list,
            expected_list,
            metadata["comparison_type"],
            problem.slug
    ):
        response["result"] = "Tests passed!"
    else:
        response["result"] = "Tests failed!"

    return
