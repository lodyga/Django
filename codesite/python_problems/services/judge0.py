import json
import requests
import socket
from codesite.auth.judge0_auth import JUDGE0_API_KEY
from .ui_problem_test_cases import get_problem_metadata, get_problem_type_name
from .problem_test_case_parsing import compare_output_and_expected, get_field, serialize
from .code_assembly import clean_types, attach_utils, attach_validation_payload

def is_localhost():
    # localhost_list = ["127.0.0.1", "127.0.1.1", "::1"]
    hostname = socket.gethostname()
    # host_ip = socket.gethostbyname(hostname)
    return hostname == "GF108"


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
    ).json() or None

    return response


def check_for_response_error(response):
    if not response:
        return "No response from judge0."

    # handles C++ response["error"]
    elif "error" in response:
        return response["error"]

    # handles Java response["compile_output"]
    elif response["compile_output"] is not None:
        return response["compile_output"]

    elif response["status"]["id"] in (1, 2, 3, 4, 5, 6):
        return response["status"]["description"]

    else:
        return response["stderr"]


def get_results(response, expected_serialized_list, problem, language):
    stdout = response["stdout"]
    output_serialized_list = stdout.strip().splitlines()
    metadata = get_problem_metadata(problem)
    comparison_type = metadata.get("comparison_type", problem.comparison_type)
    N = len(expected_serialized_list)
    # expected_serialized_list form paramters is outdated, to be removed after metadata is complete

    output_value_list = [
        json.loads(line)
        for line in output_serialized_list[-N: ]
    ]
    
    expected_value_list = []
    problem_test_cases = problem.get_shared_testcases(include_hidden=True) or None
    
    if not problem_test_cases:
        raise ValueError("No problem test cases found.")
    
    for problem_test_case in problem_test_cases:
        expected = get_field(problem_test_case.data, "expected")
        expected_value_list.append(expected)


    if compare_output_and_expected(
        output_value_list,
        expected_value_list,
        comparison_type,
        language
    ):
        return "Tests passed!"
    else:
        return "Tests failed!"


def execute_code(problem, source_code, language, button_pressed="run", test_cases=""):
    problem_type = get_problem_type_name(problem)
    metadata = get_problem_metadata(problem)
    is_in_place = metadata.get("in_place", False)

    source_code = clean_types(source_code)
    source_code = attach_utils(
        source_code,
        language,
        problem_type,
        is_in_place
    )
    source_code, expected_serialized_list = attach_validation_payload(
        source_code, problem, language, test_cases, button_pressed
    )
    response = run_judge0(source_code, language)

    if (err := check_for_response_error(response)) != "Accepted":
        return err

    if button_pressed == "run":
        return response["stdout"]

    return get_results(response, expected_serialized_list, problem, language)

# response["stdout"]:
# '[0, 1]\n[1, 2]\n[0, 1]\n'
# '[0,1]\n[1,2]\n[0,1]\n'
# '[4, 7, 2, 9, 6, 3, 1]\n[2, 3, 1]\n[]\n[7, 15, 3, 20, 9]\n'

# bool, str, int, floar
# list[], list[list[]]
# ListNode
# TreeNode
