import copy

def run_tests(method):
    for input_data in inputs_list:
        data_copy = copy.deepcopy(input_data)
        # method = getattr(solution, method_name)
        method(*data_copy)
        print(json.dumps(*data_copy))


# run_tests(solution.moveZeroes)
