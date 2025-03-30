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

def get_placeholder_source_code(language_id):
        """
        Set default `Hello, world!` source code.
        """
        placeholder_source_code = ""
        if language_id == 1:
            placeholder_source_code = """# Python (3.8.1)\r\n\r\nfrom typing import Optional, List  # Use types from typing\n\r\nclass Solution:\r\n\tdef fun(self, x: str) -> str:\r\n\t\treturn x\r\n\r\nsolution = Solution()\r\nprint(solution.fun("Hello, World!"))"""
        elif language_id == 2:
            placeholder_source_code = """// JavaScript (Node.js 12.14.0)\r\n\r\nclass Solution {\r\n  fun(x) {\r\n    return x\r\n  }\r\n}\r\n\r\nconst solution = new Solution();\r\nconsole.log(solution.fun('Hello, World!'))"""
        elif language_id == 6:
            placeholder_source_code = """// Java (OpenJDK 13.0.1)\r\n\r\npublic class Main {\r\n    public static void main(String[] args) {\r\n        System.out.println("Hello, World!");\r\n    }\r\n}"""
        elif language_id == 7:
            placeholder_source_code = """// C++ (GCC 9.2.0)\r\n\r\n#include <iostream>\r\nusing namespace std;\r\n\r\nint main() {\r\n  cout << "Hello, World!";\r\n  return 0;\r\n}"""
        elif language_id == 3:
            placeholder_source_code = """# Python (3.8.1)\r\nimport pandas as pd\r\n\r\n"""
        elif language_id == 4:
            placeholder_source_code = """SELECT *\r\nFROM *\r\nWHERE *"""
        elif language_id == 5:
            placeholder_source_code = """SELECT *\r\nFROM *\r\nWHERE *"""
        else:
            placeholder_source_code = """Not known programming language."""
        return placeholder_source_code