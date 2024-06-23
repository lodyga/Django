import multiprocessing


SAFE_BUILTINS = {
    # 'print': print,
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'range': range,
    'str': str,
    'int': int,
    'float': float,
    'list': list,
    'dict': dict,
    'tuple': tuple,
    'set': set,
    'bool': bool,
    '__build_class__': __build_class__,
    '__name__': __name__,
    'enumerate': enumerate,
    'ord': ord,
}

def execute_code(code):
    def code_execution(code, result_queue):
        local_vars = {}
        global_vars = {'__builtins__': SAFE_BUILTINS}
        try:
            exec(code, global_vars, local_vars)
            result_queue.put(local_vars.get("output", "No output variable found"))
        except NameError as e:
            result_queue.put(f"{type(e).__name__}: {str(e)}, Name not registered for security reasons.")
        except Exception as e:
            result_queue.put(f"Error: {str(e)} ")
    # Create a multiprocessing Queue to receive the result from the child process
    result_queue = multiprocessing.Queue()

    # Create a child process to execute the code
    process = multiprocessing.Process(
        target=code_execution, args=(code, result_queue))

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
        result = result_queue.get()

        return result
    finally:
        # Ensure that the child process is terminated
        if process.is_alive():
            process.terminate()
            process.join()



import multiprocessing
import subprocess
import os
import tempfile

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
            result = subprocess.run(docker_command, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                result_queue.put(result.stdout)
            else:
                result_queue.put(f"Error: {result.stderr}")
        except subprocess.TimeoutExpired:
            result_queue.put("Error: Execution timed out")
        finally:
            os.remove(temp_script_path)

    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=code_execution, args=(code, result_queue))

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

# Example usage:
# code = """
# output = 'Hello, Docker World!'
# print(output)
# """
# print(execute_code(code))  # Should safely execute the code and return 'Hello, Docker World!'




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
