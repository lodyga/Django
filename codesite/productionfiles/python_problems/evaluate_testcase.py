# Get the code from the textarea
code = request.POST.get('code_area', '')


# Define the test cases
test_cases = [
    ('input1', 'expected_output1'),
    ('input2', 'expected_output2'),
    # Add more test cases as needed
]

# Execute the code in a safe environment
exec_globals = {}
exec_locals = {}
try:
    exec(code, exec_globals, exec_locals)
except Exception as e:
    # Handle any errors that occur during execution
    error_message = str(e)
    # Handle the error message appropriately, e.g., display it to the user
    # or log it for debugging purposes

# Evaluate the results against the test cases
results = {}
for input_data, expected_output in test_cases:
    try:
        output = exec_locals['method_name'](input_data)  # Assuming 'method_name' is defined in the code
        results[input_data] = {
            'expected_output': expected_output,
            'output': output,
            'pass': output == expected_output
        }
    except KeyError:
        # Handle the case where 'method_name' is not defined in the code
        results[input_data] = {
            'error': "method_name not defined"
        }
    except Exception as e:
        # Handle any other exceptions that may occur during evaluation
        results[input_data] = {
            'error': str(e)
        }

# Pass the results to the template for display
context = {
    'results': results
}
