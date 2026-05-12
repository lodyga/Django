# def test_input(cls, operations: list[str], arguments: list[list]) -> list[str | int | None]:
def test_input(cls, operations: list[str], arguments: list[list]):
    res = []

    for operation, argument in zip(operations, arguments):
        # Constructor
        if operation == cls.__name__:
            instance = cls(*argument)
            res.append(None)
            continue

        # Method call
        method = getattr(instance, operation)
        result = method(*argument)
        res.append(result)

    return res

# Run tests
def run_tests(
        cls,
        operations_list: list[list[str]],
        arguments_list: list[list[list[int]]],
        show_output: bool = False
) -> list[bool]:
    """
    Run a batch of TimeMap tests and compare outputs with expected results.
    If show_output is True, returns [(actual, expected), ...] instead of booleans.
    """
    res = []

    for operations, arguments in zip(operations_list, arguments_list):
        # res.append(
        #     test_input(cls, operations, arguments)
        # )
        # Prints every test case in the new line.
        print(json.dumps(test_input(cls, operations, arguments)))

    # return res


# run_tests(MinStack, operations_list, arguments_list)
