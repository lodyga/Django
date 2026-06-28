import re
from django.conf import settings
from python_problems.models import ProblemType
from .languages import get_language_name, LANGUAGE_ADAPTERS
from .test_case_parsing import get_field, serialize
from .test_case_expression import get_test_case_input_expression


def clean_types(source_code):
    """Convert types to match Python 3.8"""
    source_code = re.sub(
        r"list\[",
        "List[",
        source_code
    )
    source_code = re.sub(
        r"tuple\[",
        "Tuple[",
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

    if language_name == "Cpp":
        source_code = attach_cpp_print(source_code)

    if is_in_place:
        source_code = source_code + "\n" + \
            get_utility(
                adapter.in_place_utils_file,
                "utils"
            ) + "\n"

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
                + "from typing import Optional, List, Tuple\n"
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


def attach_main(source_code, main_payload_list, language, method_name):
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
        "\n".join(main_payload_list) + "\n"

    match language_name:
        case "Python" | "JavaScript":
            return main_payload
        case "Cpp":
            return "int main() {\n" + main_payload + "return 0;\n" + "}\n"
        case "Java":
            return "public class Main {\n" + "public static void main(String[] args) {\n" + main_payload + "}}\n"
        case _:
            return ""


def attach_cpp_print(source_code):
    utility = get_utility("print_in_cpp.cpp", "services")
    return source_code + utility


def build_validation_payload(problem, source_code, language, metadata) -> str:
    # test_cases [('solution.twoSum([2, 7, 11, 15], 9)', '[0, 1]'), ...]
    # =>
    # 'print(json.dumps(solution.twoSum([2, 7, 11, 15], 9)))'
    # C++: print(solution.twoSum({ 2, 7, 11, 15 }, 9));
    # Java: System.out.println(Arrays.toString(solution.twoSum(new int[] {2, 7, 11, 15}, 9)));

    test_case_input = get_test_case_input_expression(problem, language)
    method_name = metadata["method_name"]
    language_name = get_language_name(language)
    adapter = LANGUAGE_ADAPTERS[language_name]
    test_case_expressions = []

    for input_data in test_case_input:
        match language_name:
            case "Python" | "JavaScript":
                tc = adapter.print_call(adapter.serialize_call(input_data))
            case "Cpp":
                tc = adapter.print_call(input_data) + ";"
            case "Java":
                tc = adapter.print_call(
                    adapter.serialize_call(input_data)
                ) + ";"
            case _:
                tc = ""

        test_case_expressions.append(tc)

    main_block = attach_main(
        source_code,
        test_case_expressions,
        language,
        method_name,
    )

    return source_code + main_block


def get_cpp_type_tuple(parameters: list) -> str:
    """
    list[int] -> tuple<vector<int>>
    list[list[int]] -> tuple<vector<vector<int>>>
    """
    if not parameters:
        return ""

    types = []

    for parameter in parameters:
        data_type = parameter["type"]

        data_type = re.sub(r"str", "string", data_type)
        data_type = re.sub(r"list\[", "vector<", data_type)
        data_type = re.sub(r"\]", ">", data_type)

        types.append(data_type)

    return "tuple<" + ", ".join(types) + ">"


def build_validation_in_place_payload(source_code, language, test_cases, metadata):
    method_name = metadata["method_name"]
    parameters = metadata["parameters"]
    language_name = get_language_name(language)
    adapter = LANGUAGE_ADAPTERS[language_name]
    inputs_list = []
    expected_list = []

    for test_case in test_cases.all():
        inputs_list.append(get_field(test_case.data, "inputs"))
        expected_list.append(get_field(test_case.data, "expected"))

    if language_name in ("Python", "JavaScript"):
        main_payload_list = (
            [
                f'{adapter.naming.inputs_list} = {serialize(inputs_list, language)}',
                f'{adapter.run_tests_function}(solution.{method_name})'
            ]
        )
    else:  # elif language_name == "Cpp":
        cpp_type_tuple = get_cpp_type_tuple(parameters)
        main_payload_list = (
            [
                "using TestCase = " + cpp_type_tuple + ";",
                f"vector<TestCase> {adapter.naming.inputs_list} = {serialize(inputs_list, language)};",
                f"{adapter.run_tests_function}(solution, &Solution::{method_name}, inputs_list);"
            ]
        )

    main_block = attach_main(
        source_code,
        main_payload_list,
        language,
        method_name,
    )

    return source_code + main_block


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

    return updated_code


def attach_validation_payload(problem, source_code, language, button_pressed):
    if button_pressed == "run":
        return source_code

    metadata = problem.metadata
    problem_type = metadata["problem_type"]

    if metadata.get("in_place", False):
        source_code = build_validation_in_place_payload(
            source_code,
            language,
            problem.testcases,
            metadata,
        )
    elif problem_type == ProblemType.CLASS:
        source_code = build_validation_class_payload(
            source_code,
            language,
            problem.testcases,
            metadata
        )
    else:
        source_code = build_validation_payload(
            problem,
            source_code,
            language,
            metadata,
        )

    return source_code


def attach_problem_type_header(source_code, problem_type, language):
    """
    Return problem type definition snippet.
    """
    language_name = get_language_name(language)
    header = ""

    match problem_type:
        case ProblemType.BINARY_TREE:
            match language_name:
                case "Python":
                    header = get_utility("binary_tree_header.py", "utils")
                case "JavaScript":
                    header = get_utility("binary-tree-header.js", "utils")

        case ProblemType.LINKED_LIST:
            match language_name:
                case "Python":
                    header = get_utility("linked_list_header.py", "utils")
                case "JavaScript":
                    header = get_utility("linked-list-header.js", "utils")

    return header + source_code


def get_placeholder_hello(language):
    """
    Set default `Hello, world!` placeholder.
    """
    match language.id:
        case 1:
            placeholder_hello = """# Python (3.8.1)\n\nclass Solution:\n\tdef fun(self, x: str) -> str:\n\t\treturn x\n\nsolution = Solution()\nprint(solution.fun("Hello, World!"))"""
        case 2:
            placeholder_hello = """// JavaScript (Node.js 12.14.0)\n\nclass Solution {\n  fun(x) {\n    return x\n  }\n}\n\nconst solution = new Solution();\nconsole.log(solution.fun('Hello, World!'))"""
        case 6:
            placeholder_hello = """// Java (OpenJDK 13.0.1)\nimport java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}"""
        case 7:
            placeholder_hello = """// C++ (GCC 9.2.0)\n\n#include <iostream>\nusing namespace std;\n\nint main() {\n  cout << "Hello, World!";\n  return 0;\n}"""
        case 3:
            placeholder_hello = """# Python (3.8.1)\nimport pandas as pd\n\n"""
        case 4:
            placeholder_hello = """SELECT *\nFROM *\nWHERE *"""
        case 5:
            placeholder_hello = """SELECT *\nFROM *\nWHERE *"""
        case 8:
            placeholder_hello = """// TypeScript (3.7.4)\n\nclass Solution {\n  fun(x) {\n    return x\n  }\n}\n\nconst solution = new Solution();\nconsole.log(solution.fun('Hello, World!'))"""
        case _:
            placeholder_hello = """Not known programming language."""

    return placeholder_hello
