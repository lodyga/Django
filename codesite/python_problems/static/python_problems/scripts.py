from time import sleep
import requests
import re
import socket
from .rapidapi_auth import RAPIDAPI_KEY


def parse_test_cases(solution_test_cases):
    """
    Parse each test case into input and output part.
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

        try:
            input_test_case = ""
            output_test_case = ""
            seen_brackets = []

            for index, char in enumerate(raw_test_case[1:-1], 1):
                if (char == "," and
                        not seen_brackets):
                    output_test_case = raw_test_case[index + 1:-1].strip()
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

    return test_cases


def parse_url(raw_url):
    return re.search(r"((https?)://)?(www\.)?(app\.)?(\w+\.\w+)(/)?", raw_url).group(5)


def is_localhost():
    # localhost_list = ["127.0.0.1", "127.0.1.1", "::1"]
    hostname = socket.gethostname()
    # host_ip = socket.gethostbyname(hostname)
    return hostname == "GF108"


def execute_code_by_judge0(source_code, language):
    language_name_to_id = {
        "Python": 71,
        "JavaScript": 63,
        "Java": 62,
        "C++": 54,
    }
    language_id = language_name_to_id[language]

    host_url = "http://localhost:2358" if is_localhost() else "https://judge0-ce.p.rapidapi.com"

    # Submit code
    submissions_url = host_url + "/submissions"
    headers = {
        "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    json = {
        "source_code": source_code,
        "language_id": language_id
    }
    response = requests.post(
        submissions_url, json=json, headers=headers).json()
    token = response["token"]

    # Fetch results
    # token = "455d43a3-e959-4ff6-91c7-a5215fd390be"  # for test
    response_url = f"{submissions_url}/{token}"
    status_id = 1
    while status_id in (1, 2):
        sleep(0.5)
        response = requests.get(response_url, headers=headers).json()
        if "error" in response:  # handles C++ response["error"]
            return response["error"]
        status_id = response["status"]["id"]

    if status_id == 3:
        stdout = response["stdout"]
        return stdout
    else:
        stderr = response["stderr"]
        return stderr
