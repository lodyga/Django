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


class Grid(TemplateView):
    template_name = "animations/grid.html"
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

        test_case = self.default_test_case
        order = self.default_order or []

        ROWS = 1 + max(row for row, _ in order) if order else 0
        COLS = 1 + max(col for _, col in order) if order else 0

        context.update({
            "order": order,
            "test_case": test_case,
            "rows": ROWS,
            "cols": COLS,
        })
        return context

    def post(self, request, *args, **kwargs):
        source_code = inspect.getsource(self.algorithm)

        raw_order_input = request.POST.get("order_input") or ""
        raw_test_case_input = request.POST.get("test_case_input") or ""
        raw_test_case_input = raw_test_case_input.strip().replace("'", '"')

        context = self.get_context_data()

        try:
            test_case = json.loads(raw_test_case_input)

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
            ROWS = COLS = 0

        context.update({
            "order": order,
            "test_case": test_case,
            "rows": ROWS,
            "cols": COLS,
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
    template_name = "animations/queue.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
