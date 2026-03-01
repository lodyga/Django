import json
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from python_problems.static.python_problems.scripts import execute_code
from . import grid_dfs, grid_bfs
import inspect  # the file contents as a string


# class TestListView(View):
#     def get(self, request):
#         return render(request, "animations/animation_list.html")


class GridDfs(TemplateView):
    template_name = "animations/grid.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test_case = [["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], [
            "0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]
        order = [[0, 0], [1, 0], [1, 1], [0, 1], [2, 2], [3, 3], [3, 4]]
        ROWS = 1 + max(row for row, _ in order)
        COLS = 1 + max(col for _, col in order)

        context.update({
            "order": order,
            "test_case": test_case,
            "rows": ROWS,
            "cols": COLS,
        })
        return context

    def post(self, request, *args, **kwargs):
        source_code = inspect.getsource(grid_dfs)
        raw_order_input = request.POST.get("order_input") or ''
        raw_test_case_input = request.POST.get("test_case_input") or ''
        raw_test_case_input = raw_test_case_input.strip().replace("'", '"')
        context = self.get_context_data()
        ROWS = 0
        COLS = 0

        try:
            test_case = json.loads(raw_test_case_input)
            # test_case = "Solution().numIslands(" + str(test_case) + ")"
            code = (
                source_code
                + "\nimport json\n"
                + "print(Solution().numIslands("
                + json.dumps(test_case)
                + "))"
            )
            output = execute_code(code, "Python")
            raw_order_input = output
        except json.JSONDecodeError:
            test_case = []

        try:
            order = json.loads(raw_order_input.strip())
            ROWS = 1 + max(row for row, _ in order)
            COLS = 1 + max(col for _, col in order)
        except json.JSONDecodeError:
            order = []

        context.update({
            "order": order,
            "test_case": test_case,
            "rows": ROWS,
            "cols": COLS,
        })

        return render(request, self.template_name, context)

        # order = [[0, 0], [1, 0], [0, 1], [1, 1], [2, 2], [3, 3], [3, 4]]
        # const order = [[0, 0], [1, 0], [0, 1], [2, 0], [1, 1], [0, 2], [2, 1], [0, 3], [1, 3]]


class GridBfs(TemplateView):
    template_name = "animations/grid.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test_case = [["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], [
            "0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]]
        order = [[0, 0], [1, 0], [0, 1], [1, 1], [2, 2], [3, 3], [3, 4]]
        ROWS = 1 + max(row for row, _ in order)
        COLS = 1 + max(col for _, col in order)

        context.update({
            "order": order,
            "test_case": test_case,
            "rows": ROWS,
            "cols": COLS,
        })
        return context

    def post(self, request, *args, **kwargs):
        source_code = inspect.getsource(grid_bfs)
        raw_order_input = request.POST.get("order_input") or ''
        raw_test_case_input = request.POST.get("test_case_input") or ''
        raw_test_case_input = raw_test_case_input.strip().replace("'", '"')
        context = self.get_context_data()
        ROWS = 0
        COLS = 0

        try:
            test_case = json.loads(raw_test_case_input)
            # test_case = "Solution().numIslands(" + str(test_case) + ")"
            code = (
                source_code
                + "\nimport json\n"
                + "print(Solution().numIslands("
                + json.dumps(test_case)
                + "))"
            )
            output = execute_code(code, "Python")
            raw_order_input = output
        except json.JSONDecodeError:
            test_case = []

        try:
            order = json.loads(raw_order_input.strip())
            ROWS = 1 + max(row for row, _ in order)
            COLS = 1 + max(col for _, col in order)
        except json.JSONDecodeError:
            order = []

        context.update({
            "order": order,
            "test_case": test_case,
            "rows": ROWS,
            "cols": COLS,
        })

        return render(request, self.template_name, context)
