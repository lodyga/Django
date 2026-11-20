import json
from ast import literal_eval
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from python_problems.models import Language, Problem
from python_problems.services.judge0 import execute_code
from . import grid_dfs, grid_bfs
import inspect  # the file contents as a string


def _is_valid_test_case(test_case):
    return (
        isinstance(test_case, list)
        and bool(test_case)
        and all(isinstance(row, list) and bool(row) for row in test_case)
        and all(len(row) == len(test_case[0]) for row in test_case)
        and all(type(cell) is str and cell in ("0", "1") for row in test_case for cell in row)
    )


def _is_valid_order(order):
    return (
        isinstance(order, list)
        and all(
            isinstance(pair, list)
            and len(pair) == 2
            and all(type(coordinate) is int and coordinate >= 0 for coordinate in pair)
            for pair in order
        )
    )


class Grid(TemplateView):
    template_name = "dsa/grid.html"
    algorithm = None
    default_order = None
    default_test_case = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        source_code = inspect.getsource(self.algorithm)

        test_case_input = json.dumps(self.default_test_case)
        order = self.default_order or []

        ROWS = 1 + max(row for row, _ in order) if order else 0
        COLS = 1 + max(col for _, col in order) if order else 0

        context.update({
            "order": order,
            "test_case_input": test_case_input,
            "rows": ROWS,
            "cols": COLS,
            "source_code": source_code,
        })
        return context

    def post(self, request, *args, **kwargs):
        source_code = inspect.getsource(self.algorithm)

        raw_test_case_input = request.POST.get("test_case_input") or ""
        context = self.get_context_data()
        context["test_case_input"] = raw_test_case_input

        try:
            test_case = json.loads(raw_test_case_input)
        except json.JSONDecodeError:
            try:
                test_case = literal_eval(raw_test_case_input)
            except (SyntaxError, ValueError):
                context["test_case_error"] = "Enter a valid JSON grid."
                return render(request, self.template_name, context)

        if not isinstance(test_case, list):
            context["test_case_error"] = "Enter a valid JSON grid."
            return render(request, self.template_name, context)

        if not _is_valid_test_case(test_case):
            context["test_case_error"] = (
                "Enter a non-empty rectangular list of rows containing only "
                'the strings "0" and "1".'
            )
            return render(request, self.template_name, context)

        problem = Problem.objects.get(slug="number-of-islands")
        language = Language.objects.get(name="Python")
        source_code += (
            "\nimport json\n"
            "print(json.dumps(Solution().numIslands("
            + json.dumps(test_case)
            + ")))\n"
        )
        output = execute_code(
            problem,
            source_code,
            language.name,
            "run",
        )

        if not isinstance(output, dict):
            context["test_case_error"] = "The solver returned an unexpected response."
            return render(request, self.template_name, context)

        if "error" in output:
            context["test_case_error"] = output["error"]
            return render(request, self.template_name, context)

        status_data = output.get("status")
        if not isinstance(status_data, dict):
            context["test_case_error"] = "The solver returned an unexpected response."
            return render(request, self.template_name, context)

        status = status_data.get("description")
        if status != "Accepted":
            context["test_case_error"] = (
                output.get("stderr")
                or output.get("result")
                or f"Execution did not complete successfully ({status or 'unknown status'})."
            )
            return render(request, self.template_name, context)

        stdout = output.get("stdout")
        if not isinstance(stdout, str):
            context["test_case_error"] = "The solver returned an invalid input path."
            return render(request, self.template_name, context)

        try:
            order = json.loads(stdout)
        except json.JSONDecodeError:
            context["test_case_error"] = "The solver returned an invalid input path."
            return render(request, self.template_name, context)

        if not _is_valid_order(order):
            context["test_case_error"] = "The solver returned an invalid input path."
            return render(request, self.template_name, context)

        ROWS = 1 + max(row for row, _ in order) if order else 0
        COLS = 1 + max(col for _, col in order) if order else 0

        context.update({
            "cols": COLS,
            "order": order,
            "rows": ROWS,
        })

        return render(request, self.template_name, context)


class GridDfs(Grid):
    algorithm = grid_dfs
    default_order = [
        [0, 0], [1, 0], [1, 1], [0, 1],
        [2, 2], [3, 3], [3, 4]
    ]


class GridBfs(Grid):
    algorithm = grid_bfs
    default_order = [
        [0, 0], [1, 0], [0, 1], [1, 1],
        [2, 2], [3, 3], [3, 4]
    ]


class Queue(TemplateView):
    template_name = "dsa/queue.html"


class Stack(TemplateView):
    template_name = "dsa/stack.html"


class Deque(TemplateView):
    template_name = "dsa/deque.html"


class LinkedList(TemplateView):
    template_name = "dsa/linked_list.html"
