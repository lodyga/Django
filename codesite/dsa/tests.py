from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, TestCase

from .views import GridDfs


class GridDfsTests(TestCase):
    def test_grid_displays_source_code_with_code_mirror_assets(self):
        response = GridDfs.as_view()(RequestFactory().get("/"))
        response.render()

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("dsa/code-mirror.js", content)
        self.assertIn(
            "<textarea id=\"gridAlgorithmContentContainer\">", content)
        self.assertIn("class Solution:", content)
        self.assertIn("def numIslands(", content)

    def test_post_calls_execute_code_with_problem_and_language(self):
        problem = SimpleNamespace(slug="number-of-islands")
        language = SimpleNamespace(name="Python")
        request = RequestFactory().post(
            "/",
            {
                "test_case_input": '[["1"]]',
            },
        )

        with (
            patch(
                "dsa.views.Problem.objects.get",
                return_value=problem,
            ) as get_problem,
            patch(
                "dsa.views.Language.objects.get",
                return_value=language,
            ) as get_language,
            patch(
                "dsa.views.execute_code",
                return_value={
                    "status": {"description": "Accepted"},
                    "stdout": "[[0, 0]]",
                },
            ) as execute_code,
        ):
            response = GridDfs.as_view()(request)

        self.assertEqual(response.status_code, 200)
        get_problem.assert_called_once_with(slug="number-of-islands")
        get_language.assert_called_once_with(name="Python")
        execute_code.assert_called_once()
        args = execute_code.call_args.args
        self.assertIs(args[0], problem)
        self.assertIn(
            'print(json.dumps(Solution().numIslands([["1"]])))',
            args[1],
        )
        self.assertEqual(args[2:], ("Python", "run"))
        self.assertIn('id="inputPath"', response.content.decode())
        self.assertIn('>[[0, 0]]</textarea>', response.content.decode())

    def test_post_accepts_single_quoted_string_grid(self):
        request = RequestFactory().post(
            "/",
            {
                "test_case_input": "[['1', '0'], ['0', '1']]",
            },
        )

        with (
            patch(
                "dsa.views.Problem.objects.get",
                return_value=SimpleNamespace(slug="number-of-islands"),
            ),
            patch(
                "dsa.views.Language.objects.get",
                return_value=SimpleNamespace(name="Python"),
            ),
            patch(
                "dsa.views.execute_code",
                return_value={
                    "status": {"description": "Accepted"},
                    "stdout": "[[0, 0]]",
                },
            ) as execute_code,
        ):
            response = GridDfs.as_view()(request)

        self.assertEqual(response.status_code, 200)
        execute_code.assert_called_once()
        self.assertIn(
            'print(json.dumps(Solution().numIslands([["1", "0"], ["0", "1"]])))',
            execute_code.call_args.args[1],
        )

    def test_post_rejects_numeric_grid_without_running_code(self):
        request = RequestFactory().post(
            "/",
            {"test_case_input": "[[1, 0], [0, 1]]"},
        )

        with patch("dsa.views.execute_code") as execute_code:
            response = GridDfs.as_view()(request)

        self.assertEqual(response.status_code, 200)
        execute_code.assert_not_called()

    def test_post_rejects_invalid_test_case_without_running_code(self):
        request = RequestFactory().post(
            "/",
            {"test_case_input": '[["1", "2"]]'},
        )

        with patch("dsa.views.execute_code") as execute_code:
            response = GridDfs.as_view()(request)

        self.assertEqual(response.status_code, 200)
        execute_code.assert_not_called()
        self.assertIn(
            b'only the strings &quot;0&quot; and &quot;1&quot;',
            response.content,
        )
