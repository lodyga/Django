import requests
import socket
from codesite.auth.judge0_auth import JUDGE0_API_KEY
from .code_assembly import (
    clean_types,
    attach_utils,
    attach_validation_payload,
)
from .response_validation import (
    validate_response,
)
from .ui_problem_test_cases import (
    get_problem_metadata,
    get_problem_type_name,
)


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
        "TypeScript": 74,
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


def handle_response_error(response):
    if not response:
        return {"error": "No response from judge0."}

    # handles C++ response["error"]
    elif response.get("error"):
        return response

    # handles Java response["compile_output"]
    elif response.get("compile_output"):
        response["error"] = response["compile_output"]
        return response

    elif response["status"]["description"] == "Accepted":
        return None

    response["result"] = "Tests failed!"
    return response


def execute_code(
        problem,
        source_code,
        language,
        button_pressed="run",
        test_cases=""
):
    problem_type = get_problem_type_name(problem)
    metadata = get_problem_metadata(problem)
    is_in_place = metadata.get("in_place", False)

    source_code = clean_types(source_code)
    source_code = attach_utils(
        source_code,
        language,
        problem_type,
        is_in_place,
    )
    source_code = attach_validation_payload(
        problem,
        source_code,
        language,
        test_cases,
        button_pressed,
    )
    response = run_judge0(source_code, language)

    if response_error := handle_response_error(response):
        return response_error

    validate_response(
        response,
        problem,
        button_pressed,
    )

    return response
