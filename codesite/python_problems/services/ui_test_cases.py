from python_problems.models import ProblemType
from .test_case_parsing import get_field, serialize
from .previews import draw_ascii
from .problem_helpers import get_problem_metadata


def get_class_ui_test_cases(problem):
    test_cases = problem.get_shared_testcases(include_hidden=True)
    ui_test_cases = []

    for test_case in test_cases:
        operations = get_field(test_case.data, "operations")
        arguments = get_field(test_case.data, "arguments")
        expected = get_field(test_case.data, "expected")
        explanation = test_case.explanation

        if (len(operations) != len(arguments)):
            raise ValueError("Operations and arguments length mismatch.")

        display_input = ", ".join(
            f"{oper}({', '.join(map(str, arg))})"
            for (oper, arg) in zip(operations, arguments)
        )

        display_input = "(" + display_input + ")"

        ui_test_cases.append({
            "id": test_case.id,
            "owner_id": test_case.owner_id,
            "source": "shared",
            "input": display_input,
            "output": expected,
            "explanation": explanation,
        })

    return ui_test_cases


# Meaby split test cases and previes test cases?
def get_method_ui_test_cases(problem, language):
    test_cases = problem.get_shared_testcases(include_hidden=True)
    metadata = get_problem_metadata(problem)
    problem_type = metadata["problem_type"]
    parameters = metadata["parameters"]
    ui_test_cases = []

    for problem_test_case in test_cases:
        inputs = get_field(problem_test_case.data, "inputs")
        expected = get_field(problem_test_case.data, "expected")
        preview_data = []

        if (not parameters or len(parameters) != len(inputs)):
            raise ValueError("Parameters and inputs length mismatch.")

        display_input = "\n".join(
            f'{parameter["name"]} = {serialize(value, language)}'
            for parameter, value in zip(parameters, inputs)
        )

        for data, parameter in zip(inputs, parameters):
            if preview := draw_ascii(
                data,
                problem_type,
                parameter["name"],
                parameter["type"],
            ):
                preview_data.append(preview)

        if preview := draw_ascii(
            expected,
            problem_type,
            None,  # Better output type/parameter name?
            metadata["return_type"],
        ):
            preview_data.append(preview)

        expected = serialize(expected, language)
        ui_item = {
            "id": problem_test_case.id,
            "owner_id": problem_test_case.owner_id,
            "source": "shared",
            "input": display_input,
            "output": expected,
        }

        if preview_data:
            ui_item["preview"] = preview_data

        if problem_test_case.explanation:
            ui_item["explanation"] = problem_test_case.explanation

        ui_test_cases.append(ui_item)

    return ui_test_cases


def get_ui_test_cases(problem, language):
    """
    Problem TC format
    [('nums = [2, 7, 11, 15]\ntarget = 9', [0, 1]), ...]
    For binary tree preview
    [([...], [...], <serialized binary tree>), ...]
    """
    metadata = get_problem_metadata(problem)
    problem_type = metadata["problem_type"]

    if problem_type == ProblemType.CLASS:
        return get_class_ui_test_cases(problem)
    else:
        return get_method_ui_test_cases(problem, language)
