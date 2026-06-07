import json
import requests
import socket
from codesite.auth.judge0_auth import JUDGE0_API_KEY
from .ui_problem_test_cases import get_problem_metadata, get_problem_type_name
from .problem_test_case_parsing import compare_output_and_expected
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


def get_results(response, expected_output, problem, language):
    stdout = response["stdout"]
    outputs = stdout.strip().splitlines()
    metadata = get_problem_metadata(problem)
    
    # Load Python and JavaScript data using JSON.
    # C++ has wierd {} markings. Support vectors for now.
    if language in ("Python", "JavaScript"):
        parsed_outputs = [
            json.loads(line)
            for line in outputs[-len(expected_output):]
        ]
    else:
        parsed_outputs = outputs[-len(expected_output):]

    if (
        compare_output_and_expected(
            parsed_outputs,
            expected_output,
            metadata.get("comparison_type", problem.comparison_type),
            language
        ) 
        # todo
        # or
        # language == "C++" and not response["stdout"] or
        # stdout.find("rue") != -1 and stdout.find("alse") == -1
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
    source_code, expected_output = attach_validation_payload(
        source_code, problem, language, test_cases, button_pressed
    )
    response = run_judge0(source_code, language)

    if (err := check_for_response_error(response)) != "Accepted":
        return err

    if button_pressed == "run":
        return response["stdout"]

    return get_results(response, expected_output, problem, language)
