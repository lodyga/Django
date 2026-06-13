import re
from django.conf import settings
from python_problems.models import ProblemType
from .languages import get_language_name, LANGUAGE_ADAPTERS
from .problem_test_case_parsing import get_field, serialize
from .ui_problem_test_cases import get_problem_type_name, get_problem_metadata


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


def get_utility(filename, directory):
    file_path = settings \
        .BASE_DIR \
        / "python_problems/" \
        / directory \
        / filename

    with open(file_path, "r") as file:
        utility = file.read()

    return utility


def attach_utils(source_code, language, problem_type, is_in_place):
    language_name = get_language_name(language)
    adapter = LANGUAGE_ADAPTERS[language_name]

    if is_in_place:
        source_code = source_code.rstrip() + "\n" + \
            get_utility(
            adapter.in_place_utils_file,
            "utils"
        ).rstrip() + "\n"

    match problem_type:
        case ProblemType.BINARY_TREE:
            source_code = get_utility(
                adapter.binary_tree.utils_file,
                "utils"
            ) + "\n" + source_code
        case ProblemType.LINKED_LIST:
            source_code = get_utility(
                adapter.linked_list.utils_file,
                "utils"
            ) + "\n" + source_code
        case ProblemType.CLASS:
            class_utils = get_utility(
                adapter.class_design.utils_file,
                "utils"
            )
            cleaned_utils = clean_types(class_utils)
            source_code = source_code + "\n" + cleaned_utils

    match language_name:
        case "Python":
            source_code = (
                "import json\n"
                + "from typing import Optional, List\n"
                + source_code
            )
        case "JavaScript" if adapter.heap_utils_file:
            source_code = (
                get_utility(adapter.heap_utils_file, "utils")
                + source_code
            )

    return source_code


# meaby_delete_solution_instance_setup not search or raise Error
def clear_solution_instance_setup(source_code, method_name, language):
    language_name = get_language_name(language)
    adapter = LANGUAGE_ADAPTERS[language_name]
    re.sub(adapter.solution.instance_pattern, source_code, "")


# to delete
def add_solution_instance_setup(source_code, method_name, language):
    if method_name:
        language_name = get_language_name(language)
        adapter = LANGUAGE_ADAPTERS[language_name]

        if not re.search(adapter.solution.instance_pattern, source_code):
            source_code += adapter.solution.instance_code

    return source_code


def get_solution_instance_setup(source_code, method_name, language):
    if method_name:
        language_name = get_language_name(language)
        adapter = LANGUAGE_ADAPTERS[language_name]
        return adapter.solution.instance_code
    return ""


def attach_main(source_code, test_case_expressions, language, method_name):
    if not method_name or not language:
        return ""

    language_name = get_language_name(language)

    clear_solution_instance_setup(source_code, method_name, language)

    solution_instance_setup = get_solution_instance_setup(
        source_code,
        method_name,
        language
    )

    main_payload = solution_instance_setup + \
        "\n".join(test_case_expressions) + "\n"

    match language_name:
        case "Python" | "JavaScript":
            return main_payload
        case "Cpp":
            return "int main() {\n" + main_payload + "return 0;\n" + "}\n"
        case _:
            return ""


def attach_printVector(source_code):
    utility = get_utility("print_in_cpp.cpp", "services")
    return source_code + utility


def build_validation_payload(source_code, language, test_cases, method_name):
    # ('solution.twoSum([2, 7, 11, 15], 9)', '[0, 1]')
    # =>
    # 'print(json.dumps(solution.twoSum([2, 7, 11, 15], 9)))'
    # C++: print(solution.twoSum({ 2, 7, 11, 15 }, 9));

    language_name = get_language_name(language)
    adapter = LANGUAGE_ADAPTERS[language_name]
    test_case_expressions = []

    for input_data, _ in test_cases:
        match language_name:
            case "Python" | "JavaScript":
                tc = adapter.print_call(adapter.serialize_call(input_data))
            case "Cpp":
                tc = adapter.print_call(input_data) + ";"
            case _:
                tc = ""

        test_case_expressions.append(tc)

    if language_name == "Cpp":
        source_code = attach_printVector(source_code)

    main_block = attach_main(
        source_code,
        test_case_expressions,
        language,
        method_name,
    )

    source_code = source_code + main_block
    expected_output = [expected for _, expected in test_cases]

    return source_code, expected_output


def build_validation_class_payload(source_code, language, test_cases, metadata):
    language_name = get_language_name(language)
    adapter = LANGUAGE_ADAPTERS[language_name]
    operations_list = []
    arguments_list = []
    expected_list = []

    for test_case in test_cases.all():
        operations_list.append(get_field(test_case.data, "operations"))
        arguments_list.append(get_field(test_case.data, "arguments"))
        expected_list.append(get_field(test_case.data, "expected"))

    updated_code = (
        f"{source_code}\n"
        f'{adapter.naming.operations_list} = {serialize(operations_list, language)}\n'
        f'{adapter.naming.arguments_list} = {serialize(arguments_list, language)}\n'
        f'{adapter.run_tests_function}({metadata["class_name"]}, 'f'{adapter.naming.operations_list}, {adapter.naming.arguments_list})\n'
    )
    expected_output = [serialize(expected, language)
                       for expected in expected_list]

    return updated_code, expected_output


def build_validation_in_place_payload(source_code, language, test_cases, method_name):
    language_name = get_language_name(language)
    adapter = LANGUAGE_ADAPTERS[language_name]
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
        f'{adapter.naming.inputs_list} = {serialize(inputs_list, language)}\n'
        f'{adapter.run_tests_function}(solution.{method_name})\n'
    )
    expected_output = [serialize(expected, language)
                       for expected in expected_list]

    return updated_code, expected_output


def attach_validation_payload(source_code, problem, language, test_cases, button_pressed):
    if button_pressed == "run":
        return source_code, []

    problem_type = get_problem_type_name(problem)
    metadata = get_problem_metadata(problem)

    if metadata.get("in_place", False):
        source_code, expected_output = build_validation_in_place_payload(
            source_code,
            language,
            problem.testcases,
            metadata["method_name"]
        )

    elif problem_type == ProblemType.CLASS:
        source_code, expected_output = build_validation_class_payload(
            source_code,
            language,
            problem.testcases,
            metadata
        )

    else:
        source_code, expected_output = build_validation_payload(
            source_code,
            language,
            test_cases,
            metadata["method_name"],
        )

    return source_code, expected_output


def get_problem_type_header(problem_type, language):
    """
    Return problem type definition snippet.
    """
    language_name = get_language_name(language)

    match problem_type:
        case ProblemType.BINARY_TREE:
            match language_name:
                case "Python":
                    return '''# class TreeNode:\n#     """\n#     Definition for a binary tree node.\n#     """\n#     def __init__(self, val=None, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\n\n\n'''
                case "JavaScript":
                    return """/**\n * class TreeNode {\n *    constructor(val = null, left = null, right = null) {\n *       this.val = val\n *       this.left = left\n *       this.right = right\n *    };\n * }\n */\n\n\n"""

        case ProblemType.LINKED_LIST:
            match language_name:
                case "Python":
                    return '''# class ListNode:\n#     """\n#     Definition for singly-linked list.\n#     """\n#     def __init__(self, val=None, next=None):\n#         self.val = val\n#         self.next = next\n\n\n'''
                case "JavaScript":
                    return """/**\n * Represents a node in a singly-linked list.\n * class ListNode {\n *    constructor(val = null, next = null) {\n *       this.val = val;\n *       this.next = next;\n *    }\n * }\n */\n\n\n"""

    return ""


def get_placeholder_source_code(language):
    """
    Set default `Hello, world!` placeholder.
    """
    match language.id:
        case 1:
            placeholder_source_code = """# Python (3.8.1)\n\nclass Solution:\n\tdef fun(self, x: str) -> str:\n\t\treturn x\n\nsolution = Solution()\nprint(solution.fun("Hello, World!"))"""
        case 2:
            placeholder_source_code = """// JavaScript (Node.js 12.14.0)\n\nclass Solution {\n  fun(x) {\n    return x\n  }\n}\n\nconst solution = new Solution();\nconsole.log(solution.fun('Hello, World!'))"""
        case 6:
            placeholder_source_code = """// Java (OpenJDK 13.0.1)\nimport java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}"""
        case 7:
            placeholder_source_code = """// C++ (GCC 9.2.0)\n\n#include <iostream>\nusing namespace std;\n\nint main() {\n  cout << "Hello, World!";\n  return 0;\n}"""
        case 3:
            placeholder_source_code = """# Python (3.8.1)\nimport pandas as pd\n\n"""
        case 4:
            placeholder_source_code = """SELECT *\nFROM *\nWHERE *"""
        case 5:
            placeholder_source_code = """SELECT *\nFROM *\nWHERE *"""
        case _:
            placeholder_source_code = """Not known programming language."""

    return placeholder_source_code
