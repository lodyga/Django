from time import sleep
import requests
import multiprocessing
import re
import socket
from RestrictedPython import compile_restricted
from RestrictedPython import safe_builtins, limited_builtins, utility_builtins, safe_globals
from RestrictedPython.Eval import default_guarded_getitem, default_guarded_getiter
from RestrictedPython.PrintCollector import PrintCollector
from RestrictedPython.Guards import guarded_unpack_sequence, guarded_iter_unpack_sequence, full_write_guard, safer_getattr
from .rapidapi_auth import RAPIDAPI_KEY


def execute_code(source_code):
    def code_execution(source_code, result_queue):
        local_vars = {}
        try:
            byte_code = compile_restricted(
                source_code, filename='<inline code>', mode='exec')

            # Define the allowed built-ins and globals
            restricted_globals = safe_globals.copy()

            restricted_globals.update({
                '__builtins__': safe_builtins.copy()
            })

            restricted_globals['__builtins__'].update({
                'dict': dict,
                'list': list,
                'map': map,
                'filter': filter,
                'all': all,
                'any': any,
                'sum': sum,
                'min': min,
                'max': max,
                'round': round,
                'type': type,
                '__build_class__': __build_class__,  # Allow class creation
                '__metaclass__': type,  # Allow metaclass
                '__name__': __name__,
            })

            restricted_globals.update({
                '_getiter_': default_guarded_getiter,
                '_getitem_': default_guarded_getitem,
                '_getattr_': safer_getattr,
                '_print_': PrintCollector,
                '_unpack_sequence_': guarded_unpack_sequence,
                '_iter_unpack_sequence_': guarded_iter_unpack_sequence,
                '_write_': full_write_guard,
            })

            exec(byte_code, restricted_globals, local_vars)
            result_queue.put(local_vars.get(
                "output", "No output variable found"))
        # except NameError as e:
        #     result_queue.put(f"{type(e).__name__}: {str(e)}, not registered for security reasons.")
        # except ImportError as e:
        #     result_queue.put(f"{type(e).__name__}: {str(e)}, not registered for security reasons.")
        except Exception as e:
            result_queue.put(f"Error: {str(e)}")
    # Create a multiprocessing Queue to receive the result from the child process
    result_queue = multiprocessing.Queue()

    # Create a child process to execute the code
    process = multiprocessing.Process(
        target=code_execution, args=(source_code, result_queue))

    try:
        # Start the child process
        process.start()

        # Wait for the process to finish or timeout after 10 seconds
        process.join(timeout=5)

        # Check if the process is still alive (i.e., if it timed out)
        if process.is_alive():
            # Terminate the process if it's still running
            process.terminate()
            process.join()

            # Return an error message indicating timeout
            return "Error: Execution timed out"

        # Retrieve the result from the Queue
        if not result_queue.empty():
            result = result_queue.get()
        else:
            result = "Error: No result returned"

        return result
    finally:
        # Ensure that the child process is terminated
        if process.is_alive():
            process.terminate()
            process.join()


def parse_testcases(solution_test_cases):
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
            input_test_case = "Invalid testcase input"
            output_test_case = "Invalid testcase output"
        finally:
            test_cases.append((input_test_case, output_test_case))

    return test_cases


def parse_url(raw_url):
    return re.search(r"((https?)://)?(www\.)?(app\.)?(\w+\.\w+)(/)?", raw_url).group(5)


def is_localhost():
    localhost_list = ["127.0.0.1", "127.0.1.1", "::1"]
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    return host_ip in localhost_list


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
