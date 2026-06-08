from python_problems.models import ProblemType
from .problem_test_case_parsing import get_field, serialize, get_solution_problem_test_cases
from .previews import draw_ascii, unpack_linked_list_payload
from .languages import get_language_name, LANGUAGE_ADAPTERS


def get_class_ui_problem_test_cases(problem_test_cases):
    ui_problem_test_cases = []

    for problem_test_case in problem_test_cases:
        operations = get_field(problem_test_case.data, "operations")
        arguments = get_field(problem_test_case.data, "arguments")
        expected = get_field(problem_test_case.data, "expected")
        explanation = problem_test_case.explanation

        if (len(operations) == len(arguments)):
            display_input = ", ".join(
                f"{op}({', '.join(map(str, ar))})"
                for (op, ar) in zip(operations, arguments)
            )
            display_input = "(" + display_input + ")"
        else:
            display_input = (operations, arguments)

        ui_problem_test_cases.append({
            "id": problem_test_case.id,
            "owner_id": problem_test_case.owner_id,
            "source": "shared",
            "input": display_input,
            "output": expected,
            "explanation": explanation,
        })

    return ui_problem_test_cases


def get_meta_ui_problem_test_cases(problem, language, problem_test_cases):
    ui_problem_test_cases = []
    metadata = get_problem_metadata(problem)
    problem_type = get_problem_type_name(problem)
    parameters = metadata["parameters"]

    for problem_test_case in problem_test_cases:
        inputs = get_field(problem_test_case.data, "inputs")
        expected = get_field(problem_test_case.data, "expected")

        if (parameters and len(parameters) == len(inputs)):
            display_input = "\n".join(
                f'{parameter["name"]} = {serialize(value, language)}'
                for parameter, value in zip(parameters, inputs)
            )
        else:
            display_input = inputs

        preview_data = []
        if inputs:
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
            None,
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
        ui_problem_test_cases.append(ui_item)

    return ui_problem_test_cases


def get_problem_metadata(problem):
    return problem.metadata or {}


def get_problem_type_name(problem):
    metadata = get_problem_metadata(problem)

    if metadata:
        return metadata.get("problem_type") or problem.problem_type
    return problem.problem_type


def get_no_meta_ui_problem_test_cases(problem, language, problem_test_cases):
    ui_problem_test_cases = []
    problem_type = get_problem_type_name(problem)
    argument_names = problem.argument_names or []

    for problem_test_case in problem_test_cases:
        inputs = get_field(problem_test_case.data, "inputs")
        expected = get_field(problem_test_case.data, "expected")

        if (argument_names and len(argument_names) == len(inputs)):
            display_input = "\n".join(
                f"{name} = {serialize(value, language)}"
                for name, value in zip(argument_names, inputs)
            )
        else:
            display_input = inputs

        preview_data = []
        if inputs and argument_names:
            for data, argument_name in zip(inputs, argument_names):
                if preview := draw_ascii(
                    data,
                    problem_type,
                    argument_name,
                    None
                ):
                    preview_data.append(preview)

        if preview := draw_ascii(
            expected,
            problem_type,
            "res",
            None
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
        ui_problem_test_cases.append(ui_item)

    return ui_problem_test_cases


# todelete
def get_solution_ui_problem_test_cases(solution):
    solution_problem_test_cases = get_solution_problem_test_cases(
        solution.test_cases)
    ui_problem_test_cases = []

    for problem_test_case in solution_problem_test_cases:
        inputs, expected = problem_test_case

        if inputs.startswith("Solution()"):
            inputs = inputs[11:]

        ui_item = {
            "id": None,
            "owner_id": None,
            "source": "solution_fallback",
            "input": inputs,
            "output": expected,
        }

        ui_problem_test_cases.append(ui_item)

    return ui_problem_test_cases


def get_ui_problem_test_cases(problem, solution, language):
    """
    Problem TC format
    [('nums = [2, 7, 11, 15]\ntarget = 9', [0, 1]), ...]
    For binary tree preview
    [([...], [...], <serialized binary tree>), ...]
    """

    problem_test_cases = problem.get_shared_testcases(include_hidden=True)

    if problem_test_cases:
        problem_type = get_problem_type_name(problem)

        if problem_type == ProblemType.CLASS:
            return get_class_ui_problem_test_cases(problem_test_cases)

        elif get_problem_metadata(problem):
            return get_meta_ui_problem_test_cases(problem, language, problem_test_cases)

        elif problem_type:
            return get_no_meta_ui_problem_test_cases(problem, language, problem_test_cases)

        else:
            return []

    # todelete
    elif solution.test_cases:
        return get_solution_ui_problem_test_cases(solution)

    return []


def build_problem_test_case_expression(problem, problem_test_case_data, language):
    """
    problem_test_case_data["inputs"] = [[2, 7, 11, 15], 9]
    =>
    'solution.twoSum([[2, 7, 11, 15], 9])'

    'serialize_binary_tree(solution.invertTree(build_binary_tree([4, 2, 7, 1, 3, 6, 9])))'
    'serialize_linked_list(solution.reverseList(build_linked_list([1, 2, 3, 4, 5])))'
    """

    language_name = get_language_name(language)
    adapter = LANGUAGE_ADAPTERS[language_name]
    metadata = get_problem_metadata(problem)

    if metadata:
        if not metadata["parameters"] or not metadata["method_name"] or not metadata["return_type"]:
            return None

        inputs = get_field(problem_test_case_data, "inputs")
        parameters = metadata["parameters"]
        method_name = metadata["method_name"]
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

    else:
        method_name = problem.method_name
        if not method_name:
            return None

        inputs = get_field(problem_test_case_data, "inputs")

        serialized_inputs = ", ".join(
            serialize(value, language)
            for value in inputs
        )
        res = f"solution.{method_name}({serialized_inputs})"
        return res


def get_problem_problem_test_cases(problem, language):
    """
    [('solution.twoSum([2, 7, 11, 15], 9)', '[0, 1]'), ...]
    or

    """
    problem_problem_test_cases = []

    for problem_test_case in problem.get_shared_testcases(include_hidden=True):
        expression = build_problem_test_case_expression(
            problem,
            problem_test_case.data,
            language,
        )

        if not expression:
            continue

        expected = serialize(
            get_field(problem_test_case.data, "expected"),
            language
        )
        problem_problem_test_cases.append((expression, expected))

    return problem_problem_test_cases


def get_effective_problem_test_cases(problem, solution, language):
    """
    => [('solution.twoSum([2, 7, 11, 15], 9)', '[0, 1]'), ...]
    """
    if get_problem_type_name(problem) == ProblemType.CLASS:
        return []
    elif problem_problem_test_cases := get_problem_problem_test_cases(problem, language):
        return problem_problem_test_cases
    # todelete
    elif solution_problem_test_cases := get_solution_problem_test_cases(solution.test_cases):
        return solution_problem_test_cases
    else:
        return []


def get_clipboard_problem_test_cases(problem, solution, language):
    language_name = get_language_name(language)
    adapter = LANGUAGE_ADAPTERS[language_name]
    solution_instance_setup = adapter.solution.instance_code

    return solution_instance_setup + "\n".join(
        adapter.print_call(f"{test_input}, {expected}")
        for test_input, expected in get_effective_problem_test_cases(problem, solution, language)
    ) + "\n"
