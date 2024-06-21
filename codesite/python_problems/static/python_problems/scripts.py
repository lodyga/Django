import multiprocessing


def execute_code(code):
    # Define a function to execute the code
    def code_execution(code, result_queue):
        local_vars = {}
        global_vars = {}
        try:
            exec(code, global_vars, local_vars)
            # result_queue.put(local_vars.get("output"))
            result_queue.put(local_vars["output"])
        except Exception as e:
            result_queue.put(f"Error: {str(e)}")

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
