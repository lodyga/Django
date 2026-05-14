import ast
import binarytree
import json
import re
import requests
import socket
from collections import Counter
from time import sleep
from django.apps import apps
from django.conf import settings
from django.templatetags.static import static
from codesite.auth.judge0_auth import JUDGE0_API_KEY
from python_problems.models import Problem, ComparisonType, ProblemType


LANGUAGE_CONFIG = {
    "Python": {
        "print": "print",
        "serialize": "json.dumps",
        "instance": "\nsolution = Solution()\n",
        "instance_pattern": r"solution\s*=\s*Solution\(\)\s*",
        "binary_tree_utils": "binary_tree_utils.py",
        "build_tree": "build_tree",
        "serialize_tree": "serialize_tree",
        "linked_list_utils": "linked_list_utils.py",
        "build_list": "build_list",
        "serialize_list": "serialize_list",
        "run_tests": "run_tests",
        "inputs_list": "inputs_list",
        "class_design_utils": "class_design_utils.py",
        "operations_list": "operations_list",
        "arguments_list": "arguments_list",
        "expected_list": "expected_list",
        "in_place_utils": "in_place_utils.py",
    },
    "JavaScript": {
        "print": "console.log",
        "serialize": "JSON.stringify",
        "instance": "\nconst solution = new Solution();\n",
        "instance_pattern": r"const\s+solution\s*=\s*new\s+Solution\(\)\s*;?",
        "binary_tree_utils": "binary-tree-utils.js",
        "heap": "heap-utils.js",
        "build_tree": "buildTree",
        "serialize_tree": "serializeTree",
        "linked_list_utils": "linked-list-utils.js",
        "build_list": "buildList",
        "serialize_list": "serializeList",
        "run_tests": "runTests",
        "inputs_list": "inputsList",
        "class_design_utils": "class-design-utils.js",
        "operations_list": "operationsList",
        "arguments_list": "argumentsList",
        "expected_list": "expectedList",
        "in_place_utils": "in-place-utils.js",
    },
}


# Remove this abomination when all test cases are moved to problem.
def get_solution_test_cases(solution_test_cases):
    """
    Clean each solution test case into (input, expected output) tuple.
    str: 'print(Solution().twoSum([2, 7, 11, 15], 9) == [0, 1])\r\n'
    =>
    list: [('Solution().twoSum([2, 7, 11, 15], 9)', '[0, 1]'), ...]
    """
    if not solution_test_cases:
        return []

    test_cases = []
    for raw_test_case in solution_test_cases.splitlines():
        raw_test_case = raw_test_case.strip()

        if raw_test_case.startswith("console.log"):
            raw_test_case = raw_test_case[11:].strip()
        elif raw_test_case.startswith("print"):
            raw_test_case = raw_test_case[5:].strip()
        elif raw_test_case.startswith("System.out.println"):
            raw_test_case = raw_test_case[18:].strip()

        if raw_test_case.find("===") != -1:
            input_test_case, output_test_case = raw_test_case.split("===")
            test_cases.append((input_test_case.strip()[1:],
                               output_test_case.split(")")[0].strip()))
        elif raw_test_case.find("==") != -1:
            input_test_case, output_test_case = raw_test_case.split("==")
            test_cases.append((input_test_case.strip()[1:],
                               output_test_case.split(")")[0].strip()))
        elif (raw_test_case.count("[") == raw_test_case.count("]") and
                raw_test_case.count("(") == raw_test_case.count(")")):
            try:
                input_test_case = ""
                output_test_case = ""
                seen_brackets = []

                for index, char in enumerate(raw_test_case[1:-1], 1):
                    if (char == "," and
                            not seen_brackets):
                        output_test_case = raw_test_case[index + 1: -1].strip()
                        break

                    input_test_case += char
                    if char in "[(":
                        seen_brackets.append(char)
                    elif char in "])":
                        seen_brackets.pop()

            except:
                input_test_case = "Invalid test case input"
                output_test_case = "Invalid test case output"
            finally:
                test_cases.append((input_test_case, output_test_case))
        else:
            input_test_case, output_test_case = raw_test_case.rsplit(",")
            test_cases.append((input_test_case.strip()[1:],
                               output_test_case.strip()[:-1]))

    return test_cases


def serialize(value, language):
    """
    [2, 7, 11, 15] => '[2, 7, 11, 15]'
    """
    if language == "Python":
        return repr(value)

    return json.dumps(value)


def get_field(data, key):
    if isinstance(data, dict):
        return data[key]

    elif isinstance(data, list):
        idx_map = {
            "inputs": 0,
            "expected": 1 if len(data) == 2 else 2,
            "operations": 0,
            "arguments": 1,
        }
        return data[idx_map[key]]


def is_grid_shape(data):
    if not data:
        return

    for row in data:
        if len(row) != len(data[0]):
            return
        if not row:
            return

    return True


def draw_grid(data, parameter_name):
    if not is_grid_shape(data):
        return

    rows = len(data)
    cols = len(data[0])
    chars = {str(char) for line in data for char in line}
    char_map = {}

    if all(char.isalpha() for char in chars):
        return

    match len(chars):
        case 1 | 2 | 3:
            char_map = {
                "-1": "█",
                "0": "·",
                "1": "■",
                "2": "X",
                "2147483647": "∞",
            }
        case _:
            char_map = {char: char for char in chars}
            char_map["-1"] = "█"

    grid = """┌""" + "─" * (cols*2 + 1) + "┐\n"

    for line in data:
        grid_line = "".join(
            char_map.get(str(char), "J")
            for char in line
        )
        grid = grid + "│ " + " ".join(grid_line) + " │\n"

    grid = grid + """└""" + "─" * (cols*2 + 1) + "┘"

    return (parameter_name, grid)


def draw_tree(data, parameter_name):
    bt = binarytree.build2(data).__str__()
    parameter_name = parameter_name or "root"
    return (parameter_name, bt)


def draw_linked_list(data, parameter_name):
    preview = ("(" + ") -> (".join(map(str, data)) + ")")if data else "null"
    return (parameter_name, preview)


def draw_list(heights, parameter_name):
    if not heights:
        return ""

    fill = "█"
    max_height = max(heights)
    lines = []

    for level in range(max_height, 0, -1):
        row = f"{level:>2} | "

        for h in heights:
            if h >= level:
                row += f"{fill} "
            else:
                row += "  "

        lines.append(row.rstrip())

    axis = "   +" + "-" * (2 * len(heights) + 1)
    indexes = "     " + " ".join(str(i) for i in range(len(heights)))

    lines.append(axis)
    lines.append(indexes)

    return (parameter_name, "\n".join(lines))


def draw_ascii(data, problem_type, parameter_name, parameter_type):
    """
    █▓▒░#║╬■⬛🧱~≈∼≋≀·○🌊💧■▲◆●⬤⛰GO⊙✦★
    """
    match parameter_type:
        case ProblemType.BINARY_TREE:
            return draw_tree(data, parameter_name)
        case ProblemType.LINKED_LIST:
            return draw_linked_list(data, parameter_name)
        case "list[int]":
            return draw_list(data, parameter_name)
        # todo grid?
        case "list[list[int]]" | "grid":
            return draw_grid(data, parameter_name)

    if problem_type == ProblemType.BINARY_TREE and isinstance(data, list):
        bt = binarytree.build2(data).__str__()
        return (parameter_name, bt)

    elif problem_type == ProblemType.LINKED_LIST and isinstance(data, list):
        return draw_linked_list(data, parameter_name)

    # for grid/matrix/board-like data
    elif problem_type not in (ProblemType.BINARY_TREE, ProblemType.LINKED_LIST) and data and isinstance(data, list) and isinstance(data[0], list):
        return draw_grid(data, parameter_name)


def get_class_ui_test_cases(problem, solution, language, test_cases):
    ui_test_cases = []

    for test_case in test_cases:
        operations = get_field(test_case.data, "operations")
        arguments = get_field(test_case.data, "arguments")
        expected = get_field(test_case.data, "expected")

        if (len(operations) == len(arguments)):
            display_input = ", ".join(
                f"{op}({', '.join(map(str, ar))})"
                for (op, ar) in zip(operations, arguments)
            )
            display_input = "(" + display_input + ")"
        else:
            display_input = (operations, arguments)

        ui_test_cases.append({
            "id": test_case.id,
            "owner_id": test_case.owner_id,
            "source": "shared",
            "input": display_input,
            "output": expected,
        })

    return ui_test_cases


def get_meta_ui_test_cases(problem, solution, language, test_cases):
    ui_test_cases = []
    metadata = problem.metadata
    problem_type = metadata["problem_type"]
    parameters = metadata["parameters"]

    for test_case in test_cases:
        inputs = get_field(test_case.data, "inputs")
        expected = get_field(test_case.data, "expected")

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
            "id": test_case.id,
            "owner_id": test_case.owner_id,
            "source": "shared",
            "input": display_input,
            "output": expected,
        }

        if preview_data:
            ui_item["preview"] = preview_data
        if test_case.explanation:
            ui_item["explanation"] = test_case.explanation
        ui_test_cases.append(ui_item)

    return ui_test_cases


def get_no_meta_ui_test_cases(problem, solution, language, test_cases):
    ui_test_cases = []
    problem_type = problem.problem_type
    argument_names = problem.argument_names

    for test_case in test_cases:
        inputs = get_field(test_case.data, "inputs")
        expected = get_field(test_case.data, "expected")

        if (argument_names and len(argument_names) == len(inputs)):
            display_input = "\n".join(
                f"{name} = {serialize(value, language)}"
                for name, value in zip(argument_names, inputs)
            )
        else:
            display_input = inputs

        preview_data = []
        if inputs:
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
            "id": test_case.id,
            "owner_id": test_case.owner_id,
            "source": "shared",
            "input": display_input,
            "output": expected,
        }

        if preview_data:
            ui_item["preview"] = preview_data
        if test_case.explanation:
            ui_item["explanation"] = test_case.explanation
        ui_test_cases.append(ui_item)

    return ui_test_cases


def get_solution_ui_test_cases(problem, solution, language, test_cases):
    solution_test_cases = get_solution_test_cases(solution.test_cases)
    ui_test_cases = []

    for test_case in solution_test_cases:
        inputs, expected = test_case

        if inputs.startswith("Solution()"):
            inputs = inputs[11:]

        ui_item = {
            "id": None,
            "owner_id": None,
            "source": "solution_fallback",
            "input": inputs,
            "output": expected,
        }

        ui_test_cases.append(ui_item)

    return ui_test_cases


def get_ui_test_cases(problem, solution, language):
    """
    Problem TC format
    [('nums = [2, 7, 11, 15]\ntarget = 9', [0, 1]), ...]
    For binary tree preview
    [([...], [...], <serialized binary tree>), ...]
    """

    test_cases = problem.get_shared_testcases(include_hidden=True)

    if test_cases:
        problem_type = problem.problem_type

        if problem_type == ProblemType.CLASS:
            return get_class_ui_test_cases(problem, solution, language, test_cases)

        elif problem.metadata:
            return get_meta_ui_test_cases(problem, solution, language, test_cases)

        elif problem_type:
            return get_no_meta_ui_test_cases(problem, solution, language, test_cases)

        else:
            return []

    elif solution.test_cases:
        return get_solution_ui_test_cases(problem, solution, language, test_cases)

    return []


def build_problem_test_case_expression(problem, test_case_data, language):
    """
    test_case_data["inputs"] = [[2, 7, 11, 15], 9]
    =>
    'solution.twoSum([[2, 7, 11, 15], 9])'

    'serialize_tree(solution.invertTree(build_tree([4, 2, 7, 1, 3, 6, 9])))'
    'serialize_list(solution.reverseList(build_list([1, 2, 3, 4, 5])))'
    """

    config = LANGUAGE_CONFIG[language]

    if problem.metadata:
        metadata = problem.metadata
        if not metadata["parameters"] or not metadata["method_name"] or not metadata["return_type"]:
            return None

        inputs = get_field(test_case_data, "inputs")
        parameters = metadata["parameters"]
        method_name = metadata["method_name"]
        return_type = metadata["return_type"]
        lines = []

        for value, parameters in zip(inputs, metadata["parameters"]):
            name, data_type = parameters["name"], parameters["type"]

            match data_type:
                case ProblemType.BINARY_TREE:
                    line = serialize(value, language)
                    line = f'{config["build_tree"]}({line})'
                case ProblemType.LINKED_LIST:
                    line = serialize(value, language)
                    line = f'{config["build_list"]}({line})'
                case _:
                    line = serialize(value, language)

            lines.append(line)

        serialized_inputs = ", ".join(lines)

        match return_type:
            case ProblemType.BINARY_TREE:
                res = f'{config["serialize_tree"]}(solution.{metadata["method_name"]}({serialized_inputs}))'
            case ProblemType.LINKED_LIST:
                res = f'{config["serialize_list"]}(solution.{metadata["method_name"]}({serialized_inputs}))'
            case _:
                res = f'solution.{metadata["method_name"]}({serialized_inputs})'

        return res

    else:
        method_name = problem.method_name
        if not method_name:
            return None

        inputs = get_field(test_case_data, "inputs")

        serialized_inputs = ", ".join(
            serialize(value, language)
            for value in inputs
        )
        res = f"solution.{method_name}({serialized_inputs})"
        return res


def get_problem_test_cases(problem, language):
    """
    [('solution.twoSum([2, 7, 11, 15], 9)', '[0, 1]'), ...]
    or

    """
    problem_test_cases = []

    for test_case in problem.get_shared_testcases(include_hidden=True):
        expression = build_problem_test_case_expression(
            problem,
            test_case.data,
            language,
        )

        if not expression:
            continue

        expected = serialize(
            get_field(test_case.data, "expected"),
            language
        )
        problem_test_cases.append((expression, expected))

    return problem_test_cases


def get_class_test_cases(problem, language):
    return []


def get_effective_test_cases(problem, solution, language):
    """
    => [('solution.twoSum([2, 7, 11, 15], 9)', '[0, 1]'), ...]
    """
    if problem.problem_type == ProblemType.CLASS:
        return get_class_test_cases(problem, language)
    elif problem_test_cases := get_problem_test_cases(problem, language):
        return problem_test_cases
    elif solution_test_cases := get_solution_test_cases(solution.test_cases):
        return solution_test_cases
    else:
        return []


def get_clipboard_test_cases(problem, solution, language):
    config = LANGUAGE_CONFIG[language]
    solution_instance_setup = config["instance"]

    return solution_instance_setup + "\n".join(
        f'{config["print"]}({test_input}, {expected})'
        for test_input, expected in get_effective_test_cases(problem, solution, language)
    ) + "\n"


def parse_url(raw_url):
    return re.search(r"((https?)://)?(www\.)?(app\.)?(\w+\.\w+)(/)?", raw_url).group(5)


def clean_types(source_code):
    """Convert types to match Python 3.8"""
    source_code = re.sub(
        r"list\[",
        "List[",
        source_code
    )
    source_code = re.sub(
        r"TreeNode\s*\|\s*None\s*",
        "Optional[TreeNode]",
        source_code
    )
    source_code = re.sub(
        r"ListNode\s*\|\s*None\s*",
        "Optional[ListNode]",
        source_code
    )
    return source_code


def get_utility(utility_type, language):
    config = LANGUAGE_CONFIG[language]
    filename = config[utility_type]

    file_path = settings \
        .BASE_DIR \
        / "python_problems/utils" \
        / filename

    with open(file_path, "r") as file:
        utility = file.read()

    return utility


def attach_utils(source_code, language, problem_type, is_in_place):
    if is_in_place:
        source_code = source_code.rstrip() + "\n" + get_utility(
            "in_place_utils", language).rstrip() + "\n"

    match problem_type:
        case ProblemType.BINARY_TREE:
            source_code = get_utility(
                "binary_tree_utils", language) + "\n" + source_code
        case ProblemType.LINKED_LIST:
            source_code = get_utility(
                "linked_list_utils", language) + "\n" + source_code
        case ProblemType.CLASS:
            class_utils = get_utility("class_design_utils", language)
            cleaned_utils = clean_types(class_utils)
            source_code = source_code + "\n" + cleaned_utils

    match language:
        case "Python":
            source_code = (
                "import json\n"
                + "from typing import Optional, List\n"
                + source_code
            )
        case "JavaScript":
            source_code = (
                get_utility("heap", language)
                + source_code
            )

    return source_code


def add_solution_instance_setup(source_code, method_name, language):
    if method_name:
        config = LANGUAGE_CONFIG[language]

        if not re.search(config["instance_pattern"], source_code):
            source_code += config["instance"]

    return source_code


def build_validation_payload(source_code, language, test_cases, metadata):
    # ('solution.twoSum([2, 7, 11, 15], 9)', '[0, 1]')
    # =>
    # 'print(json.dumps(solution.twoSum([2, 7, 11, 15], 9)))'

    config = LANGUAGE_CONFIG[language]
    test_case_expressions = [
        f'{config["print"]}({config["serialize"]}({input_data}))'
        for input_data, _ in test_cases
    ]
    updated_code = source_code.rstrip() + "\n" + "\n".join(test_case_expressions) + "\n"
    expected_output = [expected for _, expected in test_cases]

    return updated_code, expected_output


def is_localhost():
    # localhost_list = ["127.0.0.1", "127.0.1.1", "::1"]
    hostname = socket.gethostname()
    # host_ip = socket.gethostbyname(hostname)
    return hostname == "GF108"


def freeze(value):
    if isinstance(value, list):
        return tuple(freeze(item) for item in value)

    if isinstance(value, dict):
        return tuple(sorted(
            (key, freeze(val))
            for key, val in value.items()
        ))

    return value


def compare_output_and_expected(output, expected, comparison_type, language):
    """
    Need ast.literal_eval() to compare:
    raw_item: P: '[0, 1]'
              JS: '[ 0, 1 ]'
    expected_raw_item: P '[0, 1]'
                       JS: '[0, 1]'

    raw_item: P: 'True'
              JS: 'true'
    expected_raw_item: P: 'True'
                      JS: 'true'
    """
    if len(output) != len(expected):
        return False

    for item, expected_raw_item in zip(output, expected):
        match language:
            # "True" => True
            case "Python":
                try:
                    expected_item = ast.literal_eval(expected_raw_item)
                except (ValueError, SyntaxError):
                    expected_item = expected_raw_item
            # "true" => True
            case _:
                try:
                    expected_item = json.loads(expected_raw_item)
                except (ValueError, SyntaxError):
                    expected_item = expected_raw_item

        match comparison_type:
            case ComparisonType.EXACT | "equal" | "exact":
                if item != expected_item:
                    return False
            case ComparisonType.UNORDERED:
                if (
                    {freeze(x) for x in item}
                    !=
                    {freeze(x) for x in expected_item}
                ):
                    return False
                else:
                    continue
            case ComparisonType.MULTISET:
                if (
                    Counter(freeze(x) for x in item)
                    !=
                    Counter(freeze(x) for x in expected_item)
                ):
                    return False

    return True


def run_judge0(source_code, language):
    language_name_to_id = {
        "Python": 71,
        "JavaScript": 63,
        "Java": 62,
        "C++": 54,
    }

    language_id = language_name_to_id[language]

    host_url = "http://localhost:2358" if is_localhost() else "https://judge0-ce.p.rapidapi.com"

    submissions_url = host_url + "/submissions"
    headers = {
        "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
        "x-rapidapi-key": JUDGE0_API_KEY
    }

    serialized_code = {
        "source_code": source_code,
        "language_id": language_id
    }

    querystring = {
        "base64_encoded": "false",
        "wait": "true"
    }

    response = requests.post(
        submissions_url,
        json=serialized_code,
        headers=headers,
        params=querystring
    ).json()

    return response


def build_validation_class_payload(source_code, language, test_cases, metadata):
    config = LANGUAGE_CONFIG[language]
    operations_list = []
    arguments_list = []
    expected_list = []

    for test_case in test_cases.all():
        operations_list.append(get_field(test_case.data, "operations"))
        arguments_list.append(get_field(test_case.data, "arguments"))
        expected_list.append(get_field(test_case.data, "expected"))

    updated_code = (
        f"{source_code.rstrip()}\n"
        f"{config["operations_list"]} = {serialize(operations_list, language)}\n"
        f"{config["arguments_list"]} = {serialize(arguments_list, language)}\n"
        f'{config["run_tests"]}({metadata["class_name"]}, 'f"{config["operations_list"]}, {config["arguments_list"]})\n"
    )
    expected_output = [serialize(expected, language)
                       for expected in expected_list]

    return updated_code, expected_output


def build_validation_in_place_payload(source_code, language, test_cases, method_name):
    config = LANGUAGE_CONFIG[language]
    inputs_list = []
    expected_list = []

    for test_case in test_cases.all():
        inputs_list.append(get_field(test_case.data, "inputs"))
        expected_list.append(get_field(test_case.data, "expected"))

    updated_code = add_solution_instance_setup(
        source_code,
        method_name,
        language
    )
    updated_code = (
        f"{updated_code.rstrip()}\n"
        f'{config["inputs_list"]} = {serialize(inputs_list, language)}\n'
        f'{config["run_tests"]}(solution.{method_name})\n'
    )
    expected_output = [serialize(expected, language)
                       for expected in expected_list]

    return updated_code, expected_output


def attach_validation_payload(source_code, problem, language, test_cases, button_pressed):
    # Need test_cases from view because legacy test cases base on solution test cases.

    if button_pressed == "validate":
        if problem.metadata and problem.metadata.get("in_place", False):
            source_code, expected_output = build_validation_in_place_payload(
                source_code,
                language,
                problem.testcases,
                problem.metadata["method_name"]
            )

        elif problem.problem_type and problem.problem_type == ProblemType.CLASS:
            source_code, expected_output = build_validation_class_payload(
                source_code,
                language,
                problem.testcases,
                problem.metadata
            )

        else:
            source_code = add_solution_instance_setup(
                source_code,
                problem.method_name or problem.metadata["method_name"],
                language
            )
            source_code, expected_output = build_validation_payload(
                source_code,
                language,
                test_cases,
                problem.metadata
            )
    else:
        expected_output = []

    return source_code, expected_output


def check_for_response_error(response):
    if "error" in response:
        # handles C++ response["error"]
        return response["error"]
    # handles Java response["compile_output"]
    elif response["compile_output"] is not None:
        return response["compile_output"]

    status_id = response["status"]["id"]

    if status_id == 3:
        return 3
    else:
        return response["stderr"]


def get_results(expected_output, problem, language, response):
    stdout = response["stdout"]
    outputs = stdout.strip().splitlines()
    parsed_outputs = [
        json.loads(line)
        for line in outputs[-len(expected_output):]
    ]

    if (
        compare_output_and_expected(
            parsed_outputs,
            expected_output,
            problem.metadata["comparison_type"] if problem.metadata else problem.comparison_type,
            language
        ) or
        language == "C++" and not response["stdout"] or
        stdout.find("rue") != -1 and stdout.find("alse") == -1
    ):
        return "Tests passed!"
    else:
        return "Tests failed!"


def execute_code(problem, source_code, language, button_pressed="run", test_cases=""):
    is_in_place = problem.metadata.get("in_place", False)
    source_code = clean_types(source_code)
    source_code = attach_utils(
        source_code, language, problem.problem_type, is_in_place)
    source_code, expected_output = attach_validation_payload(
        source_code, problem, language, test_cases, button_pressed
    )
    response = run_judge0(source_code, language)

    if (err := check_for_response_error(response)) != 3:
        return err

    if button_pressed == "run":
        return response["stdout"]

    return get_results(expected_output, problem, language, response)


def get_placeholder_source_code(language_id):
    """
    Set default `Hello, world!` placeholder.
    """
    match language_id:
        case 1:
            placeholder_source_code = """# Python (3.8.1)\r\n\r\nclass Solution:\r\n\tdef fun(self, x: str) -> str:\r\n\t\treturn x\r\n\r\nsolution = Solution()\r\nprint(solution.fun("Hello, World!"))"""
        case 2:
            placeholder_source_code = """// JavaScript (Node.js 12.14.0)\r\n\r\nclass Solution {\r\n  fun(x) {\r\n    return x\r\n  }\r\n}\r\n\r\nconst solution = new Solution();\r\nconsole.log(solution.fun('Hello, World!'))"""
        case 6:
            placeholder_source_code = """// Java (OpenJDK 13.0.1)\r\nimport java.util.*;\r\n\r\npublic class Main {\r\n    public static void main(String[] args) {\r\n        System.out.println("Hello, World!");\r\n    }\r\n}"""
        case 7:
            placeholder_source_code = """// C++ (GCC 9.2.0)\r\n\r\n#include <iostream>\r\nusing namespace std;\r\n\r\nint main() {\r\n  cout << "Hello, World!";\r\n  return 0;\r\n}"""
        case 3:
            placeholder_source_code = """# Python (3.8.1)\r\nimport pandas as pd\r\n\r\n"""
        case 4:
            placeholder_source_code = """SELECT *\r\nFROM *\r\nWHERE *"""
        case 5:
            placeholder_source_code = """SELECT *\r\nFROM *\r\nWHERE *"""
        case _:
            placeholder_source_code = """Not known programming language."""
    return placeholder_source_code


def get_adjacent_slugs(problem):
    problem_list = Problem.objects.filter()

    problem_ids = list(problem_list.values_list("id", flat=True))

    problem_index = problem_ids.index(problem.id)

    prev_problem_id = problem_ids[problem_index - 1]

    next_problem_id = problem_ids[(problem_index + 1) % len(problem_ids)]

    prev_problem_slug = Problem.objects.filter(
        id=prev_problem_id).first().slug

    next_problem_slug = Problem.objects.filter(
        id=next_problem_id).first().slug

    return (prev_problem_slug, next_problem_slug)


def parse_problem_description(problem_description):
    if not problem_description:
        return ("", [])

    normalized = problem_description.replace("\r\n", "\n")

    def clean_segment(text):
        cleaned = re.sub(r"(?i)</?p>", "\n", text)
        cleaned = re.sub(r"(?i)<br\s*/?>", "\n", cleaned)
        cleaned = re.sub(r"(?i)</?b>", "", cleaned)
        lines = [line for line in cleaned.split("\n")]

        while lines and not lines[0]:
            lines.pop(0)
        while lines and not lines[-1]:
            lines.pop()

        if lines[0].startswith("Example "):
            lines.pop(0)
        return "\n".join(lines)

    pre_blocks = re.findall(r"(?is)<pre>(.*?)</pre>", normalized)
    question_raw = normalized.split(
        "<pre>", 1)[0] if pre_blocks else normalized

    question = clean_segment(question_raw)
    examples = []
    for block in pre_blocks:
        cleaned_block = clean_segment(block)
        if cleaned_block:
            examples.append(cleaned_block)

    return (question, examples)


def get_problem_type_header(problem_type, language):
    """
    Return problem type definition snippet.
    """
    match problem_type:
        case ProblemType.BINARY_TREE:
            match language.name:
                case "Python":
                    return '''# class TreeNode:\n#     """\n#     Definition for a binary tree node.\n#     """\n#     def __init__(self, val=None, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\n\n\n'''
                case "JavaScript":
                    return """/**\n * class TreeNode {\n *    constructor(val = null, left = null, right = null) {\n *       this.val = val\n *       this.left = left\n *       this.right = right\n *    };\n * }\n */\n\n\n"""

        case ProblemType.LINKED_LIST:
            match language.name:
                case "Python":
                    return '''# class ListNode:\n#     """\n#     Definition for singly-linked list.\n#     """\n#     def __init__(self, val=None, next=None):\n#         self.val = val\n#         self.next = next\n\n\n'''
                case "JavaScript":
                    return """/**\n * Represents a node in a singly-linked list.\n * class ListNode {\n *    constructor(val = null, next = null) {\n *       this.val = val;\n *       this.next = next;\n *    }\n * }\n */\n\n\n"""

    return ""
