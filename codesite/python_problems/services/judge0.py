import requests
from codesite.auth.rapidapi_auth import RAPIDAPI_KEY
from codesite.auth.judge0_auth import JUDGE0_AUTHN_TOKEN
from codesite.settings import (
    JUDGE0_URL,
    ENV
)
from django.core.exceptions import ValidationError
from .code_assembly import (
    clean_python_types,
    attach_utils,
    attach_validation_payload,
)
from .response_validation import (
    validate_response,
)
from .problem_helpers import (
    get_problem_metadata,
)


def run_judge0(source_code, language):
    language_name_to_id = {
        # Python (3.8.1) -> Python (3.12.13)
        "Python": 71,
        # JavaScript (Node.js 12.14.0) -> JavaScript (Node.js 22.19.0)
        "JavaScript": 63,
        # C++15 (GCC 9.2.0) -> C++17 (GCC 9.2.0)
        "C++": 54,
        "Java": 62,
        "TypeScript": 74,
    }

    language_id = language_name_to_id[language]
    submissions_url = JUDGE0_URL + "/submissions"

    if ENV == "pythonanywhere":
        headers = {
            "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
            "x-rapidapi-key": RAPIDAPI_KEY
        }
    else:
        headers = {
            "X-Auth-Token": JUDGE0_AUTHN_TOKEN
        }

    serialized_code = {
        "source_code": source_code,
        "language_id": language_id,
    }

    if language == "C++":
        serialized_code["compiler_options"] = "-std=c++17"

    querystring = {
        "base64_encoded": "false",
        "wait": "true"
    }

    raw_response = requests.post(
        submissions_url,
        json=serialized_code,
        headers=headers,
        params=querystring
    )

    if raw_response.ok is False:
        raise ValidationError(f"{raw_response.status_code}: {raw_response.reason}")

    return raw_response.json()


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
        button_pressed="run"
):
    metadata = get_problem_metadata(problem)
    problem_type = metadata["problem_type"]
    is_in_place = metadata.get("in_place", False)

    source_code = clean_python_types(source_code)
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
