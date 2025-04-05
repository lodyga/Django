import re
import requests
import socket
from time import sleep
from django.apps import apps
from django.http import JsonResponse
from .judge0_auth import JUDGE0_API_KEY
from .cohere_auth import COHERE_API_KEY


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
            input_test_case, output_test_case = raw_test_case.split("==")
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

    status_id = response["status"]["id"]

    if status_id == 3:
        stdout = response["stdout"]
        return stdout
    else:
        stderr = response["stderr"]
        return stderr


def validate_code(source_code, language, test_cases):
    expected_output = ""
    for test_case in test_cases:
        if language == "Python":
            source_code = source_code + "\r\nprint(" + str(test_case[0]) + ")"
        elif language == "JavaScript":
            source_code = source_code + \
                "\r\nconsole.log(" + str(test_case[0]) + ")"
        expected_output = expected_output + str(test_case[1]) + "\n"

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
        stdout = response["stdout"]
        if (language == "C++" and not response["stdout"] or
            stdout.find("false") == - 1 or
                stdout.endswith(expected_output)):
            return "Tests passed!"
        else:
            return "Tests failed!"
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


def store_filtered_problem_navigation_map_in_session(request, problem_list):
    filtered_problem_navigation_map = dict(
        problem_list.values_list("id", "slug"))

    # Only try to store if session is available
    if hasattr(request, 'session'):
        try:
            request.session["filtered_problem_navigation_map"] = filtered_problem_navigation_map
        except Exception as e:
            # Log but don't fail if session storage fails
            import logging
            logging.warning(f"Could not store navigation data: {str(e)}")


def get_filtered_problem_navigation_map_from_session(self):
    filtered_problem_navigation_map = self.request.session.get(
        'filtered_problem_navigation_map', {})
    filtered_problem_navigation_map = {
        int(key): val
        for key, val in filtered_problem_navigation_map.items()}
    return filtered_problem_navigation_map


def get_filtered_problem_navigation_ids_from_session(self):
    filtered_problem_navigation_map = get_filtered_problem_navigation_map_from_session(
        self)
    return sorted(filtered_problem_navigation_map.keys())


def get_adjacent_slugs(self, problem_id):
    filtered_problem_navigation_map = get_filtered_problem_navigation_map_from_session(
        self)
    filtered_problem_ids = get_filtered_problem_navigation_ids_from_session(
        self)

    # Find current index in filtered list
    current_index = None
    for index, filtered_problem_id in enumerate(filtered_problem_ids):
        if filtered_problem_id == problem_id:
            current_index = index
            break

    if current_index is not None:  # current_index might be 0
        prev_problem_id = filtered_problem_ids[current_index - 1]
        next_problem_id = filtered_problem_ids[(
            current_index + 1) % len(filtered_problem_ids)]
        prev_problem_slug = filtered_problem_navigation_map[prev_problem_id]
        next_problem_slug = filtered_problem_navigation_map[next_problem_id]
    else:
        prev_problem_slug, next_problem_slug = None, None

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
