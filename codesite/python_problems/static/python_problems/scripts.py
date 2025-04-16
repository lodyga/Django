import binarytree as tree
import re
import requests
import socket
from collections import deque
from time import sleep
from django.apps import apps
from django.conf import settings
from django.http import JsonResponse
from django.templatetags.static import static
from .judge0_auth import JUDGE0_API_KEY
from .cohere_auth import COHERE_API_KEY
from python_problems.models import Problem


def clean_test_cases(solution_test_cases):
    """
    Clean each test case into (input, output) tuple.
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


def parse_url(raw_url):
    return re.search(r"((https?)://)?(www\.)?(app\.)?(\w+\.\w+)(/)?", raw_url).group(5)


def is_localhost():
    # localhost_list = ["127.0.0.1", "127.0.1.1", "::1"]
    hostname = socket.gethostname()
    # host_ip = socket.gethostbyname(hostname)
    return hostname == "GF108"


def execute_code(source_code, language):
    source_code = get_utils(language) + source_code

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
        "x-rapidapi-key": JUDGE0_API_KEY
    }
    json = {
        "source_code": source_code,
        "language_id": language_id
    }
    querystring = {
        "base64_encoded": "false",
        "wait": "true"
    }  # Wait for execution to finish
    response = requests.post(
        submissions_url, json=json, headers=headers, params=querystring).json()
    token = response["token"]

    # Fetch results
    response_url = f"{submissions_url}/{token}"
    response = requests.get(response_url, headers=headers).json()

    if "error" in response:  # handles C++ response["error"]
        return response["error"]
    # handles Java response["compile_output"]
    elif response["compile_output"] is not None:
        return response["compile_output"]

    status_id = response["status"]["id"]

    if status_id == 3:
        stdout = response["stdout"]
        return stdout
    else:
        stderr = response["stderr"]
        return stderr


def validate_code(source_code, language, test_cases):
    source_code = get_utils(language) + source_code

    expected_output = ""
    for test_case in test_cases:
        if language == "Python":
            source_code = source_code + "\r\nprint(" + str(test_case[0]) + ")"
        elif language == "JavaScript":
            source_code = source_code + \
                "\r\nconsole.log(" + str(test_case[0]) + ")"
        expected_output = expected_output + str(test_case[1]) + "\n"
    expected_output = re.sub(r"[ \n]", "", expected_output)

    host_url = "http://localhost:2358" if is_localhost() else "https://judge0-ce.p.rapidapi.com"
    submissions_url = host_url + "/submissions"
    language_name_to_id = {
        "C++": 54,
        "Java": 62,
        "JavaScript": 63,
        "Python": 71,
    }
    language_id = language_name_to_id[language]
    json = {
        "language_id": language_id,
        "source_code": source_code,
    }
    headers = {
        "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
        "x-rapidapi-key": JUDGE0_API_KEY,
    }
    querystring = {
        "base64_encoded": "false",
        "wait": "true"
    }  # Wait for execution to finish

    # Submit code
    response = requests.post(
        submissions_url, json=json, headers=headers, params=querystring).json()
    token = response["token"]

    # Fetch results
    response_url = f"{submissions_url}/{token}"
    response = requests.get(response_url, headers=headers).json()

    if "error" in response:  # handles C++ response["error"]
        return response["error"]

    status_id = response["status"]["id"]

    if status_id == 3:
        stdout_raw = response["stdout"]
        stdout = re.sub(r"[ \n]", "", stdout_raw) if stdout_raw else stdout_raw

        if (language == "C++" and not response["stdout"] or
            stdout.endswith(expected_output) or
                stdout.find("rue") != -1 and stdout.find("alse") == -1):
            return "Tests passed!"
        else:
            return "Tests failed!"
    else:
        stderr = response["stderr"]
        return stderr


def get_utils(langeage):
    """
    Utility functions for binary tree operations.
    """
    # file_url = static("python_problems/binary_tree_utils.py")  # Gets the correct static path
    # file_path = settings.BASE_DIR / file_url
    if langeage == "Python":
        file_name = "binary_tree_utils.py"
    elif langeage == "JavaScript":
        file_name = "binary-tree-utils.js"

    file_path = settings \
        .BASE_DIR \
        / "python_problems/static/python_problems" \
        / file_name

    with open(file_path, "r") as file:
        utils = file.read()

    return utils


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
        placeholder_source_code = """// Java (OpenJDK 13.0.1)\r\nimport java.util.*;\r\n\r\npublic class Main {\r\n    public static void main(String[] args) {\r\n        System.out.println("Hello, World!");\r\n    }\r\n}"""
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


def get_problems_languages(page_number, problem_list, problems_per_page):
    """
    Returns a dictionary mapping problems to their available languages
    for the current page.

    Args:
        problem_list: Queryset of Problem objects
        page_number: Current page number (1-based)
        problems_per_page: Number of items per page

    Returns:
        Dict: {Problem: [Language, ...]}
    """
    Solution = apps.get_model("python_problems", "Solution")
    Language = apps.get_model("python_problems", "Language")
    start = (page_number - 1) * problems_per_page
    end = start + problems_per_page
    problems_languages = {}
    for problem in problem_list[start:end]:
        language_indexes = (
            Solution.objects
            .filter(problem=problem)
            .values_list("language", flat=True))
        language_list = Language.objects.filter(id__in=language_indexes)
        problems_languages[problem] = language_list
    return problems_languages


def get_adjacent_slugs(problem, language):
    problem_list = Problem.objects.filter(
        difficulty=problem.difficulty,
        solution__language=language)

    problem_ids = list(problem_list.values_list("id", flat=True))

    problem_index = problem_ids.index(problem.id)

    prev_problem_id = problem_ids[problem_index - 1]
    next_problem_id = problem_ids[(problem_index + 1) % len(problem_ids)]

    prev_problem_slug = Problem.objects.filter(
        id=prev_problem_id,
        solution__language=language).first().slug
    next_problem_slug = Problem.objects.filter(
        id=next_problem_id,
        solution__language=language).first().slug

    return (prev_problem_slug, next_problem_slug)


def get_cohere_response(user_message):
    try:
        # time.sleep(2)  # for tests
        # return JsonResponse({"response": "Waited 2 seconds."})
        headers = {
            "Authorization": f"Bearer {COHERE_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "command",
            "prompt": user_message,
        }
        response = requests.post(
            "https://api.cohere.ai/v2/generate",
            json=data,
            headers=headers,
            timeout=10
        )
        if response.status_code != 200:
            return JsonResponse({"error": f"API Error: {response.text}"}, status=response.status_code)

        ai_response = response.json()["generations"][0]["text"]
        return JsonResponse({"response": ai_response})

    except Exception as e:
        error_message = str(e)
        return JsonResponse({"error": error_message}, status=500)
