import json
from .languages import get_language_name


# todelete
def get_solution_problem_test_cases(solution_test_cases):
    # Remove this abomination when all test cases are moved to problem.
    """
    Clean each solution test case into (input, expected output) tuple.
    str: 'print(Solution().twoSum([2, 7, 11, 15], 9) == [0, 1])\n'
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


def serialize_cpp(items):
    # Serialize for C++ like json.dumps or JSON.stringify.
    """
    [2, 7, 11, 15] => '{2, 7, 11, 15}'
    """
    if isinstance(items, list):
        serialized = [serialize_cpp(item)
                      for item in items]

        return "{" + ", ".join(serialized) + "}"

    return json.dumps(items)


def serialize_java(items):
    # Serialize for C++ like json.dumps or JSON.stringify.
    """
    [2, 7, 11, 15] => 'new int[] {2, 7, 11, 15}'
    """
    if isinstance(items, list):
        serialized = [serialize_cpp(item)
                      for item in items]

        return "new int[] {" + ", ".join(serialized) + "}"

    return json.dumps(items)


def serialize(value, language) -> str:
    """
    [2, 7, 11, 15] => '[2, 7, 11, 15]'
    """
    language_name = get_language_name(language)

    match language_name:
        case "Python":
            return repr(value)
        case "JavaScript":
            return json.dumps(value)
        case "Cpp":
            return serialize_cpp(value)
        case "Java":
            return serialize_java(value)
        case _:
            return ""


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
