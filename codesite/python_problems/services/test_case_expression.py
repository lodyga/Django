from python_problems.models import ProblemType
from .test_case_parsing import get_field, serialize
from .previews import unpack_linked_list_payload
from .languages import get_language_name, LANGUAGE_ADAPTERS
from .problem_helpers import get_problem_metadata


def build_test_case_expression(problem, test_case_data, language):
    """
    test_case_data["inputs"] = [[2, 7, 11, 15], 9]
    =>
    'solution.twoSum([[2, 7, 11, 15], 9])'

    'serialize_binary_tree(solution.invertTree(build_binary_tree([4, 2, 7, 1, 3, 6, 9])))'
    'serialize_linked_list(solution.reverseList(build_linked_list([1, 2, 3, 4, 5])))'
    """

    language_name = get_language_name(language)
    adapter = LANGUAGE_ADAPTERS[language_name]
    metadata = get_problem_metadata(problem)

    inputs = get_field(test_case_data, "inputs")
    parameters = metadata["parameters"]
    return_type = metadata["return_type"]
    lines = []

    for value, parameters in zip(inputs, metadata["parameters"]):
        name, data_type = parameters["name"], parameters["type"]

        match data_type:
            case ProblemType.BINARY_TREE:
                line = serialize(value, language)
                line = f'{adapter.binary_tree.build}({line})'

            case ProblemType.LINKED_LIST:
                values, cycle_position = unpack_linked_list_payload(value)
                line = serialize(values, language)

                if language_name == "JavaScript" and cycle_position != -1:
                    line = (
                        f'{adapter.linked_list.build}'
                        f'({line}, {{ cyclePosition: {serialize(cycle_position, language)} }})'
                    )
                elif cycle_position != -1:
                    line = (
                        f'{adapter.linked_list.build}'
                        f'({line}, {serialize(cycle_position, language)})'
                    )
                else:
                    line = f'{adapter.linked_list.build}({line})'
            case _:
                line = serialize(value, language)

        lines.append(line)

    serialized_inputs = ", ".join(lines)

    match return_type:
        case ProblemType.BINARY_TREE:
            res = f'{adapter.binary_tree.serialize}(solution.{metadata["method_name"]}({serialized_inputs}))'
        case ProblemType.LINKED_LIST:
            res = f'{adapter.linked_list.serialize}(solution.{metadata["method_name"]}({serialized_inputs}))'
        case _:
            res = f'solution.{metadata["method_name"]}({serialized_inputs})'

    return res


def get_test_case_input_expression(problem, language):
    """
    ['solution.twoSum([2, 7, 11, 15], 9)', ...]
    """
    test_cases = problem.get_shared_testcases(include_hidden=True)

    return [build_test_case_expression(problem, test_case.data, language)
            for test_case in test_cases]


def get_test_case_expected_expression(problem, language):
    """
    ['[0, 1]', ...]
    """
    test_cases = problem.get_shared_testcases(include_hidden=True)
    test_case_expected = []

    for test_case in test_cases:

        expected = serialize(
            get_field(test_case.data, "expected"),
            language
        )
        test_case_expected.append(expected)

    return test_case_expected


def get_test_case_expressions(problem, language):
    """
    [('solution.twoSum([2, 7, 11, 15], 9)', '[0, 1]'), ...]
    """

    inputs_list = get_test_case_input_expression(problem, language)
    expected_list = get_test_case_expected_expression(problem, language)
    return [
        (input_data, expected)
        for input_data, expected in zip(inputs_list, expected_list)
    ]


def get_clipboard_test_cases(problem, language):
    """
    => [('solution.twoSum([2, 7, 11, 15], 9)', '[0, 1]'), ...]
    """
    metadata = get_problem_metadata(problem)
    problem_type = metadata["problem_type"]

    if problem_type == ProblemType.CLASS:
        return []

    language_name = get_language_name(language)
    adapter = LANGUAGE_ADAPTERS[language_name]
    solution_instance_setup = adapter.solution.instance_code

    test_case_expressions = "\n".join(
        adapter.print_call(f"{test_input}, {expected}")
        for test_input, expected in get_test_case_expressions(problem, language)
    ) + "\n"

    return solution_instance_setup + test_case_expressions
