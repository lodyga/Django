import ast
import json
from collections import Counter
from .languages import get_language_name
from python_problems.models import ComparisonType


def get_solution_problem_test_cases(solution_test_cases):
    # Remove this abomination when all test cases are moved to problem.
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
    language_name = get_language_name(language)

    if language_name == "Python":
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
    language_name = get_language_name(language)

    if len(output) != len(expected):
        return False

    for item, expected_raw_item in zip(output, expected):
        match language_name:
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
