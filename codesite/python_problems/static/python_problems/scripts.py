import tempfile
import os
import subprocess
import multiprocessing
from RestrictedPython import compile_restricted
from RestrictedPython import safe_builtins, limited_builtins, utility_builtins, safe_globals
from RestrictedPython.Eval import default_guarded_getitem, default_guarded_getiter
from RestrictedPython.PrintCollector import PrintCollector
from RestrictedPython.Guards import guarded_unpack_sequence, guarded_iter_unpack_sequence, full_write_guard, safer_getattr


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


def execute_code_docker(code):
    def code_execution(code, result_queue):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as temp_script:
            temp_script.write(code.encode('utf-8'))
            temp_script_path = temp_script.name

        docker_command = [
            'docker', 'run', '--rm',
            '-v', f'{temp_script_path}:/sandbox/temp_script.py:ro',
            'sandbox-image',
            'python', 'temp_script.py'
        ]

        try:
            result = subprocess.run(
                docker_command, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                result_queue.put(result.stdout)
            else:
                result_queue.put(f"Error: {result.stderr}")
        except subprocess.TimeoutExpired:
            result_queue.put("Error: Execution timed out")
        finally:
            os.remove(temp_script_path)

    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=code_execution, args=(code, result_queue))

    try:
        process.start()
        process.join(timeout=15)

        if process.is_alive():
            process.terminate()
            process.join()
            return "Error: Execution timed out"

        result = result_queue.get()
        return result
    finally:
        if process.is_alive():
            process.terminate()
            process.join()


def parse_testcases(solution_testcase):
    """ testcases parsing """

    if solution_testcase:
        # Split the test cases by newline characters
        lines = solution_testcase.split('\r\n')
    else:
        # if empty testcase
        return [], [], []

    testcases = []
    testcases_input = []
    testcases_output = []
    for line in lines:
        line = line.strip()

        if line.startswith("console.log"):
            line = line[11:]
        
        if line.startswith("print"):
            line = line[5:]

        try:
            input_part = ""
            output_part = ""
            seen_brackets = []

            for ind, char in enumerate(line[1:-1], 1):
                if char == "," and not seen_brackets:
                    output_part = line[ind + 1:-1].strip()
                    break

                input_part += char
                if char in "[(":
                    seen_brackets.append(char)
                elif char in "])":
                    seen_brackets.pop()

        except:
            input_part = "Invalid testcase"
            output_part = "Invalid testcase"
        finally:
            testcases.append((input_part, output_part))
            testcases_input.append(input_part)
            testcases_output.append(output_part)

    return testcases, testcases_input, testcases_output
