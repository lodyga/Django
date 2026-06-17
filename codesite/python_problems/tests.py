import html
import json

from django.contrib.auth import get_user_model
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.urls import reverse

from .forms import ProblemForm
from .models import (
    Complexity,
    Difficulty,
    Language,
    Problem,
    ProblemType,
    Solution,
    Tag,
    ProblemTestCase,
)
from .services.code_assembly import (
    build_validation_class_payload,
    build_validation_in_place_payload,
)
from .services.judge0 import handle_response_error
from .services.previews import draw_linked_list
from .services.ui_problem_test_cases import (
    build_problem_test_case_expression,
    get_ui_problem_test_cases,
)
from .views import ProblemIndexView


def create_sample_user(username="tester"):
    User = get_user_model()
    user, _ = User.objects.get_or_create(username=username)
    return user


def create_sample_problem(
    title="Two Sum",
    tags=None,
    difficulty=None,
    url="https://example.com",
    description="Sample problem description",
    owner=None,
):
    if tags is None:
        tags = [Tag.objects.get_or_create(name="Array")[0]]
    if difficulty is None:
        difficulty, _ = Difficulty.objects.get_or_create(name="Easy")
    if owner is None:
        owner = create_sample_user()

    problem = Problem.objects.create(
        title=title,
        difficulty=difficulty,
        url=url,
        description=description,
        owner=owner,
    )
    problem.tags.set(tags)
    return problem


def create_sample_solution(
    problem=None,
    language=None,
    owner=None,
    source_code="Simple solution.",
    test_cases="Simple test case.",
    time_complexity=None,
    space_complexity=None,
):
    if problem is None:
        problem = create_sample_problem()
    if language is None:
        language, _ = Language.objects.get_or_create(name="Python")
    if owner is None:
        owner = create_sample_user()
    if time_complexity is None:
        time_complexity, _ = Complexity.objects.get_or_create(name="O(n)")
    if space_complexity is None:
        space_complexity, _ = Complexity.objects.get_or_create(name="O(n)")

    return Solution.objects.create(
        problem=problem,
        language=language,
        owner=owner,
        source_code=source_code,
        test_cases=test_cases,
        time_complexity=time_complexity,
        space_complexity=space_complexity,
    )


def create_problem_test_case(
    problem=None,
    owner=None,
    data=None,
    is_hidden=False,
    order=1,
    explanation="",
):
    if problem is None:
        problem = create_sample_problem()
    if owner is None:
        owner = problem.owner
    if data is None:
        data = {"inputs": [[2, 7, 11, 15], 9], "expected": [0, 1]}

    return ProblemTestCase.objects.create(
        problem=problem,
        owner=owner,
        data=data,
        is_hidden=is_hidden,
        order=order,
        explanation=explanation,
    )


class BasicModelTests(TestCase):
    def test_create_tag(self):
        tag = Tag.objects.create(name="Array")

        self.assertEqual(tag.name, "Array")
        self.assertEqual(Tag.objects.count(), 1)

    def test_create_difficulty(self):
        difficulty = Difficulty.objects.create(name="Easy")

        self.assertEqual(difficulty.name, "Easy")
        self.assertEqual(Difficulty.objects.count(), 1)

    def test_create_complexity(self):
        complexity = Complexity.objects.create(name="O(1)")

        self.assertEqual(complexity.name, "O(1)")
        self.assertEqual(Complexity.objects.count(), 1)

    def test_create_language(self):
        Language.objects.all().delete()
        language = Language.objects.create(name="Python")

        self.assertEqual(language.name, "Python")
        self.assertEqual(Language.objects.count(), 1)


class ProblemModelTests(TestCase):
    def test_create_sample_problem(self):
        owner = create_sample_user()
        difficulty = Difficulty.objects.create(name="Easy")
        tags = [
            Tag.objects.create(name="Array"),
            Tag.objects.create(name="Hash Table"),
        ]

        problem = create_sample_problem(
            title="Two Sum",
            tags=tags,
            difficulty=difficulty,
            owner=owner,
        )

        self.assertEqual(problem.title, "Two Sum")
        self.assertEqual(problem.difficulty, difficulty)
        self.assertEqual(problem.owner, owner)
        self.assertCountEqual(problem.tags.all(), tags)

    def test_problem_shared_testcases_exclude_hidden_by_default(self):
        problem = create_sample_problem()
        visible = create_problem_test_case(problem=problem, order=1)
        create_problem_test_case(problem=problem, is_hidden=True, order=2)

        self.assertEqual(list(problem.get_shared_testcases()), [visible])
        self.assertEqual(problem.get_shared_testcases(include_hidden=True).count(), 2)

    def test_create_two_problems_with_same_difficulty(self):
        difficulty = Difficulty.objects.create(name="Easy")
        create_sample_problem(title="Two Sum", difficulty=difficulty)
        create_sample_problem(title="Valid Parentheses", difficulty=difficulty)

        problems = Problem.objects.order_by("id")
        self.assertEqual(problems.count(), 2)
        self.assertEqual(Difficulty.objects.count(), 1)
        self.assertEqual(problems[0].difficulty, problems[1].difficulty)


class ProblemFormTests(TestCase):
    def test_problem_form_disables_method_fields_for_class_design(self):
        form = ProblemForm(initial={"problem_type": ProblemType.CLASS})

        self.assertEqual(form.fields["method_name"].widget.attrs.get("disabled"), "disabled")
        self.assertEqual(form.fields["argument_names"].widget.attrs.get("disabled"), "disabled")

    def test_problem_form_initial_argument_names_is_json(self):
        problem = create_sample_problem()
        problem.argument_names = ["nums", "target"]  # type: ignore
        problem.save(update_fields=["argument_names"])

        form = ProblemForm(instance=problem)

        self.assertEqual(form.initial["argument_names"], '["nums", "target"]')

    def test_problem_form_saves_problem_testcases(self):
        owner = create_sample_user()
        difficulty = Difficulty.objects.create(name="Easy")
        tag = Tag.objects.create(name="Array")
        form = ProblemForm(
            data={
                "title": "Two Sum",
                "url": "https://example.com",
                "difficulty": difficulty.id,  # type: ignore
                "description": "Sample problem description",
                "tags": [tag.id],  # type: ignore
                "problem_type": ProblemType.FUNCTION,
                "method_name": "twoSum",
                "argument_names": '["nums", "target"]',
                "comparison_type": "exact",
                "shared_test_cases": (
                    '{"inputs": [[2, 7, 11, 15], 9], "expected": [0, 1]}\n'
                    '{"data": {"inputs": [[3, 2, 4], 6], "expected": [1, 2]}, '
                    '"is_hidden": true, "explanation": "Hidden case"}'
                ),
            },
            user=owner,
        )

        self.assertTrue(form.is_valid(), form.errors)

        form.instance.owner = owner
        problem = form.save()

        saved_test_cases = problem.testcases.order_by("order")
        self.assertEqual(saved_test_cases.count(), 2)
        self.assertEqual(problem.argument_names, ["nums", "target"])
        self.assertEqual(saved_test_cases[0].owner, owner)
        self.assertEqual(
            saved_test_cases[0].data,
            {"inputs": [[2, 7, 11, 15], 9], "expected": [0, 1]},
        )
        self.assertTrue(saved_test_cases[1].is_hidden)
        self.assertEqual(saved_test_cases[1].explanation, "Hidden case")

    def test_problem_form_rejects_invalid_argument_names(self):
        difficulty = Difficulty.objects.create(name="Easy")
        tag = Tag.objects.create(name="Array")
        form = ProblemForm(
            data={
                "title": "Two Sum",
                "url": "https://example.com",
                "difficulty": difficulty.id,  # type: ignore
                "description": "Sample problem description",
                "tags": [tag.id],  # type: ignore
                "problem_type": ProblemType.FUNCTION,
                "method_name": "twoSum",
                "argument_names": '{"nums": 1}',
                "comparison_type": "exact",
                "shared_test_cases": '{"inputs": [[2, 7, 11, 15], 9], "expected": [0, 1]}',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Argument names must be a JSON list.", form.errors["argument_names"])

    def test_problem_form_clears_method_fields_for_class_design(self):
        owner = create_sample_user("class-tester")
        difficulty = Difficulty.objects.create(name="Easy")
        tag = Tag.objects.create(name="Array")
        form = ProblemForm(
            data={
                "title": "Design Parking System",
                "url": "https://example.com",
                "difficulty": difficulty.id,  # type: ignore
                "description": "Sample problem description",
                "tags": [tag.id],  # type: ignore
                "problem_type": ProblemType.CLASS,
                "method_name": "shouldBeIgnored",
                "argument_names": '["ignored"]',
                "comparison_type": "exact",
                "shared_test_cases": '{"inputs": [1, 1, 0], "expected": null}',
            },
            user=owner,
        )

        self.assertTrue(form.is_valid(), form.errors)

        form.instance.owner = owner
        problem = form.save()

        self.assertEqual(problem.method_name, "")
        self.assertIsNone(problem.argument_names)

    def test_problem_form_accepts_cycle_linked_list_testcases(self):
        owner = create_sample_user("cycle-tester")
        difficulty = Difficulty.objects.create(name="Medium")
        tag = Tag.objects.create(name="Linked List")
        form = ProblemForm(
            data={
                "title": "Linked List Cycle",
                "url": "https://example.com",
                "difficulty": difficulty.id,  # type: ignore
                "description": "Detect a cycle in a linked list.",
                "tags": [tag.id],  # type: ignore
                "problem_type": ProblemType.LINKED_LIST,
                "method_name": "hasCycle",
                "argument_names": '["head"]',
                "comparison_type": "exact",
                "shared_test_cases": (
                    '{"inputs": [{"values": [3, 2, 0, -4], "cycle_position": 1}], '
                    '"expected": true}'
                ),
            },
            user=owner,
        )

        self.assertTrue(form.is_valid(), form.errors)

        form.instance.owner = owner
        problem = form.save()

        self.assertEqual(
            problem.testcases.first().data,
            {
                "inputs": [{"values": [3, 2, 0, -4], "cycle_position": 1}],
                "expected": True,
            },
        )


class Judge0ResultHandlingTests(SimpleTestCase):
    def test_handle_response_error_allows_accepted_response_to_continue(self):
        response = {
            "status": {"description": "Accepted"},
            "compile_output": None,
        }

        self.assertIsNone(handle_response_error(response))

    def test_handle_response_error_returns_response_when_no_response(self):
        self.assertEqual(
            handle_response_error(None),
            {"error": "No response from judge0."},
        )

    def test_handle_response_error_returns_existing_error_response(self):
        response = {"error": "Judge0 request failed."}

        self.assertIs(handle_response_error(response), response)

    def test_handle_response_error_converts_compile_output_to_error(self):
        response = {
            "status": {"description": "Compilation Error"},
            "compile_output": "Syntax error",
        }

        self.assertIs(handle_response_error(response), response)
        self.assertEqual(response["error"], "Syntax error")

    def test_handle_response_error_marks_non_accepted_response_as_failed(self):
        response = {
            "status": {"description": "Wrong Answer"},
            "compile_output": None,
        }

        self.assertIs(handle_response_error(response), response)
        self.assertEqual(response["result"], "Tests failed!")


class ProblemScriptTests(TestCase):
    def test_build_validation_in_place_payload_supports_move_zeroes_problem(self):
        problem = create_sample_problem(title="Move Zeroes")
        problem.metadata = {
            "problem_type": ProblemType.FUNCTION,
            "method_name": "moveZeroes",
            "parameters": [{"name": "nums", "type": "list[int]"}],
            "return_type": "None",
            "in_place": True,
        }
        problem.save(update_fields=["metadata"])

        create_problem_test_case(
            problem=problem,
            data={
                "inputs": [[0, 1, 0, 3, 12]],
                "expected": [[1, 3, 12, 0, 0]],
            },
        )

        source_code = "class Solution:\n    pass\n"
        updated_code = build_validation_in_place_payload(
            source_code,
            "Python",
            problem.testcases,
            "moveZeroes",
        )

        self.assertIn("\nsolution = Solution()\n", updated_code)
        self.assertIn("inputs_list = [[[0, 1, 0, 3, 12]]]", updated_code)
        self.assertIn("run_tests(solution.moveZeroes)", updated_code)

    def test_get_ui_test_cases_supports_number_of_islands_grid_preview(self):
        problem = create_sample_problem(title="Number of Islands")
        problem.metadata = {
            "problem_type": ProblemType.FUNCTION,
            "method_name": "numIslands",
            "parameters": [{"name": "grid", "type": "grid"}],
            "return_type": "int",
        }
        problem.save(update_fields=["metadata"])

        create_problem_test_case(
            problem=problem,
            data={
                "inputs": [[["1", "1", "0"], ["1", "0", "0"], ["0", "0", "1"]]],
                "expected": 3,
            },
        )
        solution = create_sample_solution(problem=problem)

        ui_test_cases = get_ui_problem_test_cases(problem, solution, "Python")

        self.assertEqual(len(ui_test_cases), 1)
        self.assertEqual(
            ui_test_cases[0]["input"],
            "grid = [['1', '1', '0'], ['1', '0', '0'], ['0', '0', '1']]",
        )
        self.assertEqual(ui_test_cases[0]["output"], "3")
        self.assertEqual(
            ui_test_cases[0]["preview"],
            [
                (
                    "grid",
                    "┌───────┐\n"
                    "│ ■ ■ · │\n"
                    "│ ■ · · │\n"
                    "│ · · ■ │\n"
                    "└───────┘",
                )
            ],
        )

    def test_build_validation_class_payload_supports_time_map_problem(self):
        problem = create_sample_problem(title="Time Based Key-Value Store")
        problem.problem_type = ProblemType.CLASS
        problem.metadata = {
            "problem_type": ProblemType.CLASS,
            "class_name": "TimeMap",
        }
        problem.save(update_fields=["problem_type", "metadata"])

        create_problem_test_case(
            problem=problem,
            data={
                "operations": ["TimeMap", "set", "get", "get", "set", "get", "get"],
                "arguments": [
                    [],
                    ["foo", "bar", 1],
                    ["foo", 1],
                    ["foo", 3],
                    ["foo", "bar2", 4],
                    ["foo", 4],
                    ["foo", 5],
                ],
                "expected": [None, None, "bar", "bar", None, "bar2", "bar2"],
            },
        )

        source_code = "class TimeMap:\n    pass\n"
        updated_code = build_validation_class_payload(
            source_code,
            "Python",
            problem.testcases,
            problem.metadata,
        )

        self.assertIn(
            "operations_list = [['TimeMap', 'set', 'get', 'get', 'set', 'get', 'get']]",
            updated_code,
        )
        self.assertIn(
            "arguments_list = [[[], ['foo', 'bar', 1], ['foo', 1], ['foo', 3], ['foo', 'bar2', 4], ['foo', 4], ['foo', 5]]]",
            updated_code,
        )
        self.assertIn("run_tests(TimeMap, operations_list, arguments_list)", updated_code)

    def test_build_problem_test_case_expression_supports_binary_tree_python(self):
        problem = create_sample_problem(title="Invert Binary Tree Python")
        problem.metadata = {
            "problem_type": ProblemType.BINARY_TREE,
            "method_name": "invertTree",
            "parameters": [{"name": "root", "type": ProblemType.BINARY_TREE}],
            "return_type": ProblemType.BINARY_TREE,
        }
        problem.save(update_fields=["metadata"])

        expression = build_problem_test_case_expression(
            problem,
            {"inputs": [[4, 2, 7, 1, 3, 6, 9]], "expected": [4, 7, 2, 9, 6, 3, 1]},
            "Python",
        )

        self.assertEqual(
            expression,
            "serialize_binary_tree(solution.invertTree(build_binary_tree([4, 2, 7, 1, 3, 6, 9])))",
        )

    def test_build_problem_test_case_expression_supports_linked_list_cycles_python(self):
        problem = create_sample_problem(title="Linked List Cycle Python")
        problem.metadata = {
            "problem_type": ProblemType.LINKED_LIST,
            "method_name": "hasCycle",
            "parameters": [{"name": "head", "type": ProblemType.LINKED_LIST}],
            "return_type": "bool",
        }
        problem.save(update_fields=["metadata"])

        expression = build_problem_test_case_expression(
            problem,
            {"inputs": [{"values": [3, 2, 0, -4], "cycle_position": 1}], "expected": True},
            "Python",
        )

        self.assertEqual(
            expression,
            "solution.hasCycle(build_linked_list([3, 2, 0, -4], 1))",
        )

    def test_build_problem_test_case_expression_supports_linked_list_cycles_javascript(self):
        problem = create_sample_problem(title="Linked List Cycle JavaScript")
        problem.metadata = {
            "problem_type": ProblemType.LINKED_LIST,
            "method_name": "hasCycle",
            "parameters": [{"name": "head", "type": ProblemType.LINKED_LIST}],
            "return_type": "bool",
        }
        problem.save(update_fields=["metadata"])

        expression = build_problem_test_case_expression(
            problem,
            {"inputs": [{"values": [3, 2, 0, -4], "pos": 1}], "expected": True},
            "JavaScript",
        )

        self.assertEqual(
            expression,
            "solution.hasCycle(buildLinkedList([3, 2, 0, -4], { cyclePosition: 1 }))",
        )

    def test_draw_linked_list_displays_cycle_preview(self):
        preview = draw_linked_list({"values": [3, 2, 0, -4], "cycle_position": 1}, "head")

        self.assertEqual(preview, ("head", "(3) -> (2) -> (0) -> (-4) -> ↺ index 1 (2)"))


class ProblemTestCaseCrudViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testcase-user",
            password="testpass123",
        )
        self.other_user = get_user_model().objects.create_user(
            username="other-user",
            password="testpass123",
        )
        self.client.force_login(self.user)
        self.problem = create_sample_problem(
            title="Test Case CRUD Problem",
            owner=self.user,
        )
        self.test_case = create_problem_test_case(
            problem=self.problem,
            owner=self.user,
            data={"inputs": [1], "expected": 1},
            order=1,
        )

    def test_create_test_case(self):
        response = self.client.post(
            reverse("python_problems:test_case-create"),
            data={
                "problem": self.problem.id,
                "data": json.dumps({"inputs": [2], "expected": 2}),
                "is_hidden": True,
                "order": 2,
                "explanation": "Hidden edge case",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("python_problems:problem-index"))

        created = ProblemTestCase.objects.get(problem=self.problem, order=2)
        self.assertEqual(created.owner, self.user)
        self.assertEqual(created.data, {"inputs": [2], "expected": 2})
        self.assertTrue(created.is_hidden)
        self.assertEqual(created.explanation, "Hidden edge case")

    def test_update_test_case(self):
        response = self.client.post(
            reverse("python_problems:test_case-update", kwargs={"pk": self.test_case.pk}),
            data={
                "problem": self.problem.id,
                "data": json.dumps({"inputs": [10], "expected": 10}),
                "is_hidden": False,
                "order": 3,
                "explanation": "Updated testcase",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("python_problems:problem-index"))

        self.test_case.refresh_from_db()
        self.assertEqual(self.test_case.owner, self.user)
        self.assertEqual(self.test_case.data, {"inputs": [10], "expected": 10})
        self.assertFalse(self.test_case.is_hidden)
        self.assertEqual(self.test_case.order, 3)
        self.assertEqual(self.test_case.explanation, "Updated testcase")

    def test_delete_test_case(self):
        response = self.client.post(
            reverse("python_problems:test_case-delete", kwargs={"pk": self.test_case.pk}),
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("python_problems:problem-index"))
        self.assertFalse(ProblemTestCase.objects.filter(pk=self.test_case.pk).exists())

    def test_create_requires_authentication(self):
        self.client.logout()

        response = self.client.get(reverse("python_problems:test_case-create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_update_is_owner_restricted(self):
        self.client.force_login(self.other_user)

        response = self.client.get(
            reverse("python_problems:test_case-update", kwargs={"pk": self.test_case.pk})
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_is_owner_restricted(self):
        self.client.force_login(self.other_user)

        response = self.client.post(
            reverse("python_problems:test_case-delete", kwargs={"pk": self.test_case.pk}),
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(ProblemTestCase.objects.filter(pk=self.test_case.pk).exists())


class SolutionModelTests(TestCase):
    def test_create_sample_solution(self):
        problem = create_sample_problem()
        Language.objects.all().delete()
        language = Language.objects.create(name="Python")
        owner = create_sample_user()
        time_complexity = Complexity.objects.create(name="O(n)")
        space_complexity = Complexity.objects.get(name="O(n)")

        solution = create_sample_solution(
            problem=problem,
            language=language,
            owner=owner,
            source_code="Simple solution.",
            test_cases="Simple test case.",
            time_complexity=time_complexity,
            space_complexity=space_complexity,
        )

        self.assertEqual(solution.problem, problem)
        self.assertEqual(solution.language, language)
        self.assertEqual(solution.owner, owner)
        self.assertEqual(solution.source_code, "Simple solution.")
        self.assertEqual(solution.test_cases, "Simple test case.")
        self.assertEqual(solution.time_complexity, time_complexity)
        self.assertEqual(solution.space_complexity, space_complexity)

    def test_create_two_solutions_in_different_languages_for_same_problem(self):
        language_1, _ = Language.objects.get_or_create(name="Python")
        language_2, _ = Language.objects.get_or_create(name="JavaScript")
        problem = create_sample_problem()
        create_sample_solution(problem=problem, language=language_1)
        create_sample_solution(problem=problem, language=language_2)

        solutions = Solution.objects.order_by("id")
        self.assertEqual(solutions.count(), 2)
        self.assertEqual(Language.objects.count(), 2)
        self.assertNotEqual(solutions[0].language, solutions[1].language)

    def test_create_two_solutions_in_same_language_for_different_problems(self):
        Language.objects.all().delete()
        create_sample_solution()
        create_sample_solution(problem=create_sample_problem(title="Valid Parentheses"))

        solutions = Solution.objects.order_by("id")
        self.assertEqual(solutions.count(), 2)
        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(solutions[0].language, solutions[1].language)


class ProblemIndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Language.objects.all().delete()
        cls.difficulty_easy = Difficulty.objects.create(name="Easy")
        cls.difficulty_medium = Difficulty.objects.create(name="Medium")
        cls.tag_array = Tag.objects.create(name="Array")
        cls.tag_two_pointers = Tag.objects.create(name="Two Pointers")
        cls.language_python = Language.objects.create(name="Python")
        cls.language_javascript = Language.objects.create(name="JavaScript")

        cls.problem_easy = create_sample_problem(
            title="Two Sum",
            difficulty=cls.difficulty_easy,
            tags=[cls.tag_array],
        )
        cls.problem_medium = create_sample_problem(
            title="Two Sum II - Input Array Is Sorted",
            difficulty=cls.difficulty_medium,
            tags=[cls.tag_array, cls.tag_two_pointers],
        )

        create_sample_solution(
            problem=cls.problem_easy,
            language=cls.language_python,
            source_code="print('Easy')",
        )
        create_sample_solution(
            problem=cls.problem_medium,
            language=cls.language_javascript,
            source_code="console.log('Medium')",
        )

    def test_no_problems_message(self):
        Problem.objects.all().delete()

        response = self.client.get(reverse("python_problems:problem-index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Python problems available for the given parameters.")

    def test_index_uses_template(self):
        response = self.client.get(reverse("python_problems:problem-index"))

        self.assertTemplateUsed(response, "python_problems/problem_list.html")

    def test_with_problems_displays_titles(self):
        response = self.client.get(reverse("python_problems:problem-index"))

        self.assertContains(response, "Two Sum")
        self.assertContains(response, "Two Sum II - Input Array Is Sorted")

    def test_filters_by_difficulty_with_get_parameters(self):
        response = self.client.get(
            reverse("python_problems:problem-index"),
            {"difficulty_id": self.difficulty_easy.id},
        )

        titles = [problem.title for problem in response.context["page_obj"].object_list]
        self.assertEqual(titles, ["Two Sum"])

    def test_filters_by_tag_with_get_parameters(self):
        response = self.client.get(
            reverse("python_problems:problem-index"),
            {"tag_id": self.tag_two_pointers.id},
        )

        titles = [problem.title for problem in response.context["page_obj"].object_list]
        self.assertEqual(titles, ["Two Sum II - Input Array Is Sorted"])

    def test_filters_by_query_text_with_get_parameters(self):
        response = self.client.get(
            reverse("python_problems:problem-index"),
            {"query_text": "Sorted"},
        )

        titles = [problem.title for problem in response.context["page_obj"].object_list]
        self.assertEqual(titles, ["Two Sum II - Input Array Is Sorted"])

    def test_filters_by_language_with_get_parameters(self):
        response = self.client.get(
            reverse("python_problems:problem-index"),
            {"language_id": self.language_python.id},
        )

        titles = [problem.title for problem in response.context["page_obj"].object_list]
        self.assertEqual(titles, ["Two Sum"])

    def test_ordering_and_pagination_use_page_object(self):
        for index in range(15):
            create_sample_problem(title=f"Problem {index}")

        response = self.client.get(
            reverse("python_problems:problem-index"),
            {"order_by": "title", "problems_per_page": 5, "page": 2},
        )

        page_titles = [problem.title for problem in response.context["page_obj"].object_list]
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(response.context["page_obj"].paginator.per_page, 5)
        self.assertEqual(page_titles, sorted(page_titles))

    def test_request_factory_get_request_exposes_expected_context(self):
        request = RequestFactory().get(reverse("python_problems:problem-index"))
        request.user = create_sample_user()

        response = ProblemIndexView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("page_obj", response.context_data)
        self.assertIn("problem_list", response.context_data)
        self.assertEqual(response.context_data["difficulty_id"], 0)
        self.assertEqual(response.context_data["language_id"], 0)
        self.assertEqual(response.context_data["tag_id"], 0)
        self.assertEqual(response.context_data["query_text"], "")
        self.assertEqual(response.context_data["order_by"], "created_at")


class SolutionDetailViewTests(TestCase):
    def test_right_template(self):
        solution = create_sample_solution()

        response = self.client.get(
            reverse(
                "python_problems:problem-detail",
                kwargs={"slug": solution.problem.slug, "language": solution.language.name},
            )
        )

        self.assertTemplateUsed(response, "python_problems/problem_detail.html")

    def test_context_data_uses_selected_solution(self):
        solution = create_sample_solution()

        response = self.client.get(
            reverse(
                "python_problems:problem-detail",
                kwargs={"slug": solution.problem.slug, "language": solution.language.name},
            )
        )

        self.assertEqual(response.context["problem"], solution.problem)
        self.assertEqual(response.context["solution"], solution)
        self.assertIn(solution, response.context["owner_solutions"])

    def test_owner_solution_languages_use_preferred_order(self):
        owner = create_sample_user()
        problem = create_sample_problem(owner=owner)
        languages = [
            Language.objects.get_or_create(name="Ruby")[0],
            Language.objects.get_or_create(name="Java")[0],
            Language.objects.get_or_create(name="C#")[0],
            Language.objects.get_or_create(name="C++")[0],
            Language.objects.get_or_create(name="JavaScript")[0],
            Language.objects.get_or_create(name="Python")[0],
        ]
        for language in languages:
            create_sample_solution(problem=problem, language=language, owner=owner)

        response = self.client.get(
            reverse(
                "python_problems:problem-detail",
                kwargs={"slug": problem.slug, "language": "Python"},
            )
        )

        self.assertEqual(
            [language.name for language in response.context["owner_solution_languages"]],
            ["Python", "JavaScript", "C++", "Java", "C#", "Ruby"],
        )

    def test_back_link_uses_next_url(self):
        solution = create_sample_solution()
        next_url = f"{reverse('python_problems:problem-index')}?page=2"

        response = self.client.get(
            reverse(
                "python_problems:problem-detail",
                kwargs={"slug": solution.problem.slug, "language": solution.language.name},
            ),
            {"next": next_url},
        )

        self.assertContains(response, f'href="{next_url}"')

    def test_404_response(self):
        response = self.client.get(
            reverse(
                "python_problems:problem-detail",
                kwargs={"slug": "non-existent-slug", "language": "non-existent-language"},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_problem_details_display(self):
        owner = create_sample_user()
        language, _ = Language.objects.get_or_create(name="Python")
        problem = create_sample_problem(title="Two Sum", owner=owner)
        solution = create_sample_solution(problem=problem, language=language, owner=owner)

        response = self.client.get(
            reverse(
                "python_problems:problem-detail",
                kwargs={"slug": solution.problem.slug, "language": solution.language.name},
            )
        )

        self.assertContains(response, solution.problem.title)
        self.assertContains(response, solution.problem.owner)
        self.assertContains(response, solution.language)
        self.assertContains(response, solution.owner)

    def test_problem_level_testcases_override_solution_testcases(self):
        problem = create_sample_problem()
        problem.method_name = "twoSum"
        problem.save(update_fields=["method_name"])
        solution = create_sample_solution(
            problem=problem,
            test_cases="(solution.twoSum([3, 3], 6), [0, 1])",
        )
        create_problem_test_case(
            problem=problem,
            data={"inputs": [[2, 7, 11, 15], 9], "expected": [0, 1]},
        )

        response = self.client.get(
            reverse(
                "python_problems:problem-detail",
                kwargs={"slug": problem.slug, "language": solution.language.name},
            )
        )

        self.assertContains(response, "solution.twoSum([2, 7, 11, 15], 9)")
        self.assertNotContains(response, "solution.twoSum([3, 3], 6)")
        self.assertEqual(
            response.context["effective_problem_test_cases"],
            [("solution.twoSum([2, 7, 11, 15], 9)", "[0, 1]")],
        )

    def test_problem_argument_names_label_ui_testcases(self):
        problem = create_sample_problem()
        problem.method_name = "twoSum"
        problem.argument_names = ["nums", "target"]  # type: ignore
        problem.save(update_fields=["method_name", "argument_names"])
        solution = create_sample_solution(problem=problem)
        create_problem_test_case(
            problem=problem,
            data={"inputs": [[2, 7, 11, 15], 9], "expected": [0, 1]},
        )

        response = self.client.get(
            reverse(
                "python_problems:problem-detail",
                kwargs={"slug": problem.slug, "language": solution.language.name},
            )
        )

        ui_test_case = response.context["ui_problem_test_cases"][0]
        self.assertEqual(ui_test_case["input"], "nums = [2, 7, 11, 15]\ntarget = 9")
        self.assertEqual(
            response.context["clipboard_problem_test_cases"],
            "\nsolution = Solution()\nprint(solution.twoSum([2, 7, 11, 15], 9), [0, 1])\n",
        )


class SolutionLanguageSwitchTest(TestCase):
    def setUp(self):
        Language.objects.all().delete()
        self.language_python = Language.objects.create(name="Python")
        self.language_javascript = Language.objects.create(name="JavaScript")
        self.problem = create_sample_problem()
        self.source_code_python = "print('Python solution')"
        self.source_code_javascript = "console.log('JavaScript solution');"
        create_sample_solution(
            problem=self.problem,
            language=self.language_python,
            source_code=self.source_code_python,
        )
        create_sample_solution(
            problem=self.problem,
            language=self.language_javascript,
            source_code=self.source_code_javascript,
        )

    def test_switching_language_updates_solution(self):
        url = reverse(
            "python_problems:problem-detail",
            kwargs={"slug": self.problem.slug, "language": self.language_python.name},
        )
        response = self.client.get(url)
        self.assertIn(self.source_code_python, html.unescape(response.content.decode()))

        response = self.client.post(url, {"language_id": self.language_javascript.id}, follow=True)

        self.assertIn(self.source_code_javascript, html.unescape(response.content.decode()))
        self.assertEqual(
            response.request["PATH_INFO"],
            reverse(
                "python_problems:problem-detail",
                kwargs={"slug": self.problem.slug, "language": self.language_javascript.name},
            ),
        )


class SolutionUserSwitchTest(TestCase):
    def setUp(self):
        self.language, _ = Language.objects.get_or_create(name="Python")
        self.owner_1 = create_sample_user("tester-1")
        self.owner_2 = create_sample_user("tester-2")
        self.problem = create_sample_problem()
        self.source_code_1 = "print('Python solution')"
        self.source_code_2 = "print('Python solution 2')"
        create_sample_solution(
            problem=self.problem,
            language=self.language,
            source_code=self.source_code_1,
            owner=self.owner_1,
        )
        create_sample_solution(
            problem=self.problem,
            language=self.language,
            source_code=self.source_code_2,
            owner=self.owner_2,
        )

    def test_switching_owner_updates_solution(self):
        url = reverse(
            "python_problems:problem-detail",
            kwargs={"slug": self.problem.slug, "language": self.language.name},
        )
        response = self.client.get(url)
        self.assertIn(self.source_code_1, html.unescape(response.content.decode()))

        response = self.client.post(url, {"owner_id": self.owner_2.id}, follow=True)

        self.assertIn(self.source_code_2, html.unescape(response.content.decode()))

    def test_authenticated_owner_is_selected_by_default(self):
        self.client.force_login(self.owner_2)
        url = reverse(
            "python_problems:problem-detail",
            kwargs={"slug": self.problem.slug, "language": self.language.name},
        )

        response = self.client.get(url)

        self.assertEqual(response.context["owner_id"], self.owner_2.id)
        self.assertIn(self.source_code_2, html.unescape(response.content.decode()))


# ============================================================================
# Problem CRUD View Tests
# ============================================================================


class ProblemCreateViewTests(TestCase):
    def setUp(self):
        self.user = create_sample_user("problem-creator")
        self.client.force_login(self.user)
        Language.objects.all().delete()
        Difficulty.objects.all().delete()
        Tag.objects.all().delete()
        self.language = Language.objects.create(name="Python")
        self.difficulty = Difficulty.objects.create(name="Easy")
        self.tag = Tag.objects.create(name="Array")

    def test_create_problem_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("python_problems:problem-create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_create_problem_valid_data(self):
        response = self.client.post(
            reverse("python_problems:problem-create"),
            data={
                "title": "New Problem",
                "url": "https://example.com/new",
                "difficulty": self.difficulty.id,  # type: ignore
                "description": "A new problem description",
                "tags": [self.tag.id],  # type: ignore
                "problem_type": ProblemType.FUNCTION,
                "method_name": "solve",
                "argument_names": '["nums"]',
                "comparison_type": "exact",
                "shared_test_cases": '{"inputs": [1], "expected": 1}',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Problem.objects.filter(title="New Problem").exists())
        problem = Problem.objects.get(title="New Problem")
        self.assertEqual(problem.owner, self.user)
        self.assertEqual(problem.difficulty, self.difficulty)
        self.assertEqual(problem.tags.count(), 1)

    def test_create_problem_with_class_type_clears_method_fields(self):
        response = self.client.post(
            reverse("python_problems:problem-create"),
            data={
                "title": "Class Problem",
                "url": "https://example.com/class",
                "difficulty": self.difficulty.id,  # type: ignore
                "description": "A class problem",
                "tags": [self.tag.id],  # type: ignore
                "problem_type": ProblemType.CLASS,
                "method_name": "shouldBeCleared",
                "argument_names": '["should", "be", "cleared"]',
                "comparison_type": "exact",
                "shared_test_cases": '{"inputs": [], "expected": null}',
            },
        )
        self.assertEqual(response.status_code, 302)
        problem = Problem.objects.get(title="Class Problem")
        self.assertEqual(problem.method_name, "")
        self.assertIsNone(problem.argument_names)


class ProblemUpdateViewTests(TestCase):
    def setUp(self):
        self.user = create_sample_user("problem-updater")
        self.client.force_login(self.user)
        self.problem = create_sample_problem(title="Original Title", owner=self.user)
        self.new_tag = Tag.objects.create(name="NewTag")

    def test_update_problem_requires_login(self):
        self.client.logout()
        response = self.client.get(
            reverse("python_problems:problem-update", kwargs={"pk": self.problem.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_update_problem_valid_data(self):
        response = self.client.post(
            reverse("python_problems:problem-update", kwargs={"pk": self.problem.pk}),
            data={
                "title": "Updated Title",
                "url": self.problem.url,
                "difficulty": self.problem.difficulty.id,  # type: ignore
                "description": self.problem.description,
                "tags": [self.new_tag.id],  # type: ignore
                "problem_type": ProblemType.FUNCTION,
                "method_name": "updatedMethod",
                "argument_names": '["new", "args"]',
                "comparison_type": "exact",
                "shared_test_cases": '{"inputs": [1], "expected": 1}',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.problem.refresh_from_db()
        self.assertEqual(self.problem.title, "Updated Title")
        self.assertEqual(self.problem.method_name, "updatedMethod")
        self.assertEqual(self.problem.argument_names, ["new", "args"])

    def test_update_problem_redirects_to_next_url(self):
        next_url = f"{reverse('python_problems:problem-index')}?page=2"
        response = self.client.post(
            reverse("python_problems:problem-update", kwargs={"pk": self.problem.pk}),
            data={
                "title": "Updated Title",
                "url": self.problem.url,
                "difficulty": self.problem.difficulty.id,  # type: ignore
                "description": self.problem.description,
                "tags": list(self.problem.tags.values_list("id", flat=True)),  # type: ignore
                "problem_type": ProblemType.FUNCTION,
                "method_name": "updatedMethod",
                "argument_names": '["new", "args"]',
                "comparison_type": "exact",
                "shared_test_cases": '{"inputs": [1], "expected": 1}',
                "next": next_url,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, next_url)

    def test_update_problem_with_class_type_clears_method_fields(self):
        response = self.client.post(
            reverse("python_problems:problem-update", kwargs={"pk": self.problem.pk}),
            data={
                "title": self.problem.title,
                "url": self.problem.url,
                "difficulty": self.problem.difficulty.id,  # type: ignore
                "description": self.problem.description,
                "tags": list(self.problem.tags.values_list("id", flat=True)),  # type: ignore
                "problem_type": ProblemType.CLASS,
                "method_name": "toBeCleared",
                "argument_names": '["to", "be", "cleared"]',
                "comparison_type": "exact",
                "shared_test_cases": '{"inputs": [], "expected": null}',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.problem.refresh_from_db()
        self.assertEqual(self.problem.method_name, "")
        self.assertIsNone(self.problem.argument_names)


class ProblemDeleteViewTests(TestCase):
    def setUp(self):
        self.user = create_sample_user("problem-deleter")
        self.client.force_login(self.user)
        self.problem = create_sample_problem(title="To Delete", owner=self.user)

    def test_delete_problem_requires_login(self):
        self.client.logout()
        response = self.client.post(
            reverse("python_problems:problem-delete", kwargs={"pk": self.problem.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_delete_problem(self):
        problem_id = self.problem.pk
        response = self.client.post(
            reverse("python_problems:problem-delete", kwargs={"pk": self.problem.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Problem.objects.filter(pk=problem_id).exists())

    def test_delete_problem_redirects_to_next_url(self):
        problem_id = self.problem.pk
        next_url = f"{reverse('python_problems:problem-index')}?page=2"
        response = self.client.post(
            reverse("python_problems:problem-delete", kwargs={"pk": self.problem.pk}),
            data={"next": next_url},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, next_url)
        self.assertFalse(Problem.objects.filter(pk=problem_id).exists())


# ============================================================================
# Solution CRUD View Tests
# ============================================================================


class SolutionCreateViewTests(TestCase):
    def setUp(self):
        self.user = create_sample_user("solution-creator")
        self.client.force_login(self.user)
        Language.objects.all().delete()
        self.language = Language.objects.create(name="Python")
        self.problem = create_sample_problem()

    def test_create_solution_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("python_problems:solution-create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_create_solution_valid_data(self):
        time_complexity = Complexity.objects.get_or_create(name="O(n)")[0]
        space_complexity = Complexity.objects.get_or_create(name="O(n)")[0]
        response = self.client.post(
            reverse("python_problems:solution-create"),
            data={
                "problem": self.problem.id,
                "language": self.language.id,
                "source_code": "def solve(): pass",
                "test_cases": "(solve(), None)",
                "time_complexity": time_complexity.id,
                "space_complexity": space_complexity.id,
                "order": 1,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Solution.objects.filter(
                problem=self.problem, language=self.language, owner=self.user
            ).exists()
        )

    def test_create_solution_sets_owner(self):
        time_complexity = Complexity.objects.get_or_create(name="O(n)")[0]
        space_complexity = Complexity.objects.get_or_create(name="O(n)")[0]
        response = self.client.post(
            reverse("python_problems:solution-create"),
            data={
                "problem": self.problem.id,
                "language": self.language.id,
                "source_code": "def solve(): pass",
                "test_cases": "(solve(), None)",
                "time_complexity": time_complexity.id,
                "space_complexity": space_complexity.id,
                "order": 1,
            },
        )
        self.assertEqual(response.status_code, 302)
        solution = Solution.objects.get(problem=self.problem, language=self.language, owner=self.user)
        self.assertEqual(solution.owner, self.user)


class SolutionUpdateViewTests(TestCase):
    def setUp(self):
        self.user = create_sample_user("solution-updater")
        self.client.force_login(self.user)
        Language.objects.all().delete()
        self.language = Language.objects.create(name="Python")
        self.problem = create_sample_problem()
        self.solution = create_sample_solution(
            problem=self.problem, language=self.language, owner=self.user
        )

    def test_update_solution_requires_login(self):
        self.client.logout()
        response = self.client.get(
            reverse("python_problems:solution-update", kwargs={"pk": self.solution.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_update_solution_valid_data(self):
        time_complexity = Complexity.objects.get_or_create(name="O(n)")[0]
        space_complexity = Complexity.objects.get_or_create(name="O(n)")[0]
        response = self.client.post(
            reverse("python_problems:solution-update", kwargs={"pk": self.solution.pk}),
            data={
                "source_code": "def solve(): return 42",
                "time_complexity": time_complexity.id,
                "space_complexity": space_complexity.id,
                "order": 2,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.solution.refresh_from_db()
        self.assertEqual(self.solution.source_code, "def solve(): return 42")
        self.assertEqual(self.solution.order, 2)

    def test_update_solution_is_owner_restricted(self):
        other_user = create_sample_user("other-solution-owner")
        other_solution = create_sample_solution(
            problem=self.problem, language=self.language, owner=other_user
        )

        response = self.client.get(
            reverse("python_problems:solution-update", kwargs={"pk": other_solution.pk})
        )

        self.assertEqual(response.status_code, 404)


class SolutionDeleteViewTests(TestCase):
    def setUp(self):
        self.user = create_sample_user("solution-deleter")
        self.client.force_login(self.user)
        Language.objects.all().delete()
        self.language = Language.objects.create(name="Python")
        self.problem = create_sample_problem()
        self.solution = create_sample_solution(
            problem=self.problem, language=self.language, owner=self.user
        )

    def test_delete_solution_requires_login(self):
        self.client.logout()
        response = self.client.post(
            reverse("python_problems:solution-delete", kwargs={"pk": self.solution.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_delete_solution(self):
        solution_id = self.solution.pk
        response = self.client.post(
            reverse("python_problems:solution-delete", kwargs={"pk": self.solution.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Solution.objects.filter(pk=solution_id).exists())

    def test_delete_solution_is_owner_restricted(self):
        other_user = create_sample_user("other-solution-owner")
        other_solution = create_sample_solution(
            problem=self.problem, language=self.language, owner=other_user
        )

        response = self.client.post(
            reverse("python_problems:solution-delete", kwargs={"pk": other_solution.pk})
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Solution.objects.filter(pk=other_solution.pk).exists())


# ============================================================================
# Tag CRUD View Tests
# ============================================================================


class TagViewsTests(TestCase):
    def setUp(self):
        self.user = create_sample_user("tag-manager")
        self.client.force_login(self.user)
        Tag.objects.all().delete()

    def test_tag_index_view(self):
        Tag.objects.create(name="Array")
        Tag.objects.create(name="String")
        response = self.client.get(reverse("python_problems:tag-index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Array")
        self.assertContains(response, "String")

    def test_tag_create_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("python_problems:tag-create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_tag_create_valid_data(self):
        response = self.client.post(
            reverse("python_problems:tag-create"),
            data={"name": "NewTag"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tag.objects.filter(name="NewTag").exists())

    def test_tag_update_requires_login(self):
        tag = Tag.objects.create(name="ToUpdate")
        self.client.logout()
        response = self.client.get(
            reverse("python_problems:tag-update", kwargs={"pk": tag.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_tag_update_valid_data(self):
        tag = Tag.objects.create(name="ToUpdate")
        response = self.client.post(
            reverse("python_problems:tag-update", kwargs={"pk": tag.pk}),
            data={"name": "UpdatedTag"},
        )
        self.assertEqual(response.status_code, 302)
        tag.refresh_from_db()
        self.assertEqual(tag.name, "UpdatedTag")

    def test_tag_delete_requires_login(self):
        tag = Tag.objects.create(name="ToDelete")
        self.client.logout()
        response = self.client.post(
            reverse("python_problems:tag-delete", kwargs={"pk": tag.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_tag_delete(self):
        tag = Tag.objects.create(name="ToDelete")
        tag_id = tag.pk
        response = self.client.post(
            reverse("python_problems:tag-delete", kwargs={"pk": tag.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tag.objects.filter(pk=tag_id).exists())


# ============================================================================
# Language Create View Tests
# ============================================================================


class LanguageCreateViewTests(TestCase):
    def setUp(self):
        self.user = create_sample_user("language-creator")
        self.client.force_login(self.user)
        Language.objects.all().delete()

    def test_language_create_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("python_problems:language-create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_language_create_valid_data(self):
        response = self.client.post(
            reverse("python_problems:language-create"),
            data={"name": "Rust"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Language.objects.filter(name="Rust").exists())

    def test_language_create_duplicate_name_rejected(self):
        Language.objects.create(name="Java")
        response = self.client.post(
            reverse("python_problems:language-create"),
            data={"name": "Java"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("already exists", response.content.decode().lower())
        self.assertEqual(Language.objects.count(), 1)


# ============================================================================
# ProblemTestCase CRUD View Tests
# ============================================================================


class ProblemTestCaseCreateViewTests(TestCase):
    def setUp(self):
        self.user = create_sample_user("testcase-creator")
        self.client.force_login(self.user)
        self.problem = create_sample_problem(owner=self.user)

    def test_create_test_case_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("python_problems:test_case-create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_create_test_case_valid_data(self):
        response = self.client.post(
            reverse("python_problems:test_case-create"),
            data={
                "problem": self.problem.id,
                "data": json.dumps({"inputs": [1, 2], "expected": 3}),
                "is_hidden": False,
                "order": 1,
                "explanation": "Simple addition",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ProblemTestCase.objects.filter(
                problem=self.problem, owner=self.user, order=1
            ).exists()
        )

    def test_create_test_case_sets_owner(self):
        response = self.client.post(
            reverse("python_problems:test_case-create"),
            data={
                "problem": self.problem.id,
                "data": json.dumps({"inputs": [1], "expected": 1}),
                "is_hidden": True,
                "order": 2,
                "explanation": "Hidden test",
            },
        )
        test_case = ProblemTestCase.objects.get(problem=self.problem, order=2)
        self.assertEqual(test_case.owner, self.user)


class ProblemTestCaseUpdateViewTests(TestCase):
    def setUp(self):
        self.user = create_sample_user("testcase-updater")
        self.client.force_login(self.user)
        self.problem = create_sample_problem(owner=self.user)
        self.test_case = create_problem_test_case(
            problem=self.problem, owner=self.user, order=1
        )

    def test_update_test_case_requires_login(self):
        self.client.logout()
        response = self.client.get(
            reverse("python_problems:test_case-update", kwargs={"pk": self.test_case.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_update_test_case_valid_data(self):
        response = self.client.post(
            reverse("python_problems:test_case-update", kwargs={"pk": self.test_case.pk}),
            data={
                "problem": self.problem.id,
                "data": json.dumps({"inputs": [5], "expected": 10}),
                "is_hidden": True,
                "order": 5,
                "explanation": "Updated explanation",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.test_case.refresh_from_db()
        self.assertEqual(self.test_case.data, {"inputs": [5], "expected": 10})
        self.assertTrue(self.test_case.is_hidden)
        self.assertEqual(self.test_case.order, 5)

    def test_update_test_case_owner_restriction(self):
        other_user = create_sample_user("other-user")
        other_test_case = create_problem_test_case(
            problem=self.problem, owner=other_user, order=2
        )
        response = self.client.get(
            reverse("python_problems:test_case-update", kwargs={"pk": other_test_case.pk})
        )
        self.assertEqual(response.status_code, 404)


class ProblemTestCaseDeleteViewTests(TestCase):
    def setUp(self):
        self.user = create_sample_user("testcase-deleter")
        self.client.force_login(self.user)
        self.problem = create_sample_problem(owner=self.user)
        self.test_case = create_problem_test_case(
            problem=self.problem, owner=self.user, order=1
        )

    def test_delete_test_case_requires_login(self):
        self.client.logout()
        response = self.client.post(
            reverse("python_problems:test_case-delete", kwargs={"pk": self.test_case.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_delete_test_case(self):
        test_case_id = self.test_case.pk
        response = self.client.post(
            reverse("python_problems:test_case-delete", kwargs={"pk": self.test_case.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ProblemTestCase.objects.filter(pk=test_case_id).exists())

    def test_delete_test_case_owner_restriction(self):
        other_user = create_sample_user("other-user")
        other_test_case = create_problem_test_case(
            problem=self.problem, owner=other_user, order=2
        )
        test_case_id = other_test_case.pk
        response = self.client.post(
            reverse("python_problems:test_case-delete", kwargs={"pk": other_test_case.pk})
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(ProblemTestCase.objects.filter(pk=test_case_id).exists())


# ============================================================================
# tag_graph_view Tests
# ============================================================================


class TagGraphViewTests(TestCase):
    def setUp(self):
        Tag.objects.all().delete()
        Problem.objects.all().delete()

    def test_tag_graph_view_renders(self):
        response = self.client.get(reverse("python_problems:tag-graph"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "python_problems/tag_graph.html")

    def test_tag_graph_view_shows_tag_counts(self):
        tag1 = Tag.objects.create(name="Array")
        tag2 = Tag.objects.create(name="String")
        create_sample_problem(title="Two Sum", tags=[tag1])
        create_sample_problem(title="Two Sum II", tags=[tag1])
        create_sample_problem(title="Add Strings", tags=[tag2])

        response = self.client.get(reverse("python_problems:tag-graph"))
        self.assertEqual(response.status_code, 200)
        data = response.context["data"]
        self.assertEqual(len(data), 2)
        tag1_data = next((d for d in data if d["tag"] == "Array"), None)
        tag2_data = next((d for d in data if d["tag"] == "String"), None)
        self.assertIsNotNone(tag1_data)
        self.assertIsNotNone(tag2_data)
        self.assertEqual(tag1_data["count"], 2)
        self.assertEqual(tag2_data["count"], 1)


# ============================================================================
# Model Edge Case Tests
# ============================================================================


class ProblemModelEdgeCaseTests(TestCase):
    def test_problem_slug_generation(self):
        owner = create_sample_user()
        problem = Problem.objects.create(
            title="Test Problem With Spaces",
            difficulty=Difficulty.objects.create(name="Easy"),
            url="https://example.com",
            description="Test",
            owner=owner,
        )
        self.assertEqual(problem.slug, "test-problem-with-spaces")

    def test_problem_slug_generation_with_special_chars(self):
        owner = create_sample_user()
        problem = Problem.objects.create(
            title="Test!@# Problem",
            difficulty=Difficulty.objects.create(name="Easy"),
            url="https://example.com",
            description="Test",
            owner=owner,
        )
        self.assertEqual(problem.slug, "test-problem")

    def test_problem_save_with_class_type_clears_method_fields(self):
        owner = create_sample_user()
        problem = Problem.objects.create(
            title="Class Problem",
            difficulty=Difficulty.objects.create(name="Easy"),
            url="https://example.com",
            description="Test",
            owner=owner,
            problem_type=ProblemType.CLASS,
            method_name="someMethod",
            argument_names=["arg1", "arg2"],
        )
        self.assertEqual(problem.method_name, "")
        self.assertIsNone(problem.argument_names)

    def test_problem_save_with_function_type_preserves_method_fields(self):
        owner = create_sample_user()
        problem = Problem.objects.create(
            title="Function Problem",
            difficulty=Difficulty.objects.create(name="Easy"),
            url="https://example.com",
            description="Test",
            owner=owner,
            problem_type=ProblemType.FUNCTION,
            method_name="myMethod",
            argument_names=["arg1", "arg2"],
        )
        self.assertEqual(problem.method_name, "myMethod")
        self.assertEqual(problem.argument_names, ["arg1", "arg2"])

    def test_problem_update_class_type_clears_fields(self):
        owner = create_sample_user()
        problem = Problem.objects.create(
            title="Test",
            difficulty=Difficulty.objects.create(name="Easy"),
            url="https://example.com",
            description="Test",
            owner=owner,
            problem_type=ProblemType.FUNCTION,
            method_name="myMethod",
            argument_names=["arg1"],
        )
        problem.problem_type = ProblemType.CLASS
        problem.save()
        problem.refresh_from_db()
        self.assertEqual(problem.method_name, "")
        self.assertIsNone(problem.argument_names)


class SolutionModelEdgeCaseTests(TestCase):
    def setUp(self):
        Language.objects.all().delete()
        Complexity.objects.all().delete()
        self.language = Language.objects.create(name="Python")
        self.problem = create_sample_problem()
        self.owner = create_sample_user()

    def test_solution_default_complexity(self):
        solution = Solution.objects.create(
            problem=self.problem,
            language=self.language,
            owner=self.owner,
            source_code="test",
        )
        self.assertEqual(solution.time_complexity.name, "O(n)")
        self.assertEqual(solution.space_complexity.name, "O(n)")

    def test_solution_ordering(self):
        sol1 = Solution.objects.create(
            problem=self.problem,
            language=self.language,
            owner=self.owner,
            source_code="test1",
            order=2,
        )
        sol2 = Solution.objects.create(
            problem=self.problem,
            language=self.language,
            owner=self.owner,
            source_code="test2",
            order=1,
        )
        solutions = Solution.objects.filter(problem=self.problem)
        self.assertEqual(solutions[0], sol2)
        self.assertEqual(solutions[1], sol1)


# ============================================================================
# Solution Form Tests
# ============================================================================


class SolutionFormTests(TestCase):
    def setUp(self):
        Language.objects.all().delete()
        self.language = Language.objects.create(name="Python")
        self.problem = create_sample_problem()
        self.owner = create_sample_user()

    def test_solution_create_form_valid_data(self):
        from .forms import SolutionCreateForm
        time_complexity = Complexity.objects.get_or_create(name="O(n)")[0]
        space_complexity = Complexity.objects.get_or_create(name="O(n)")[0]
        form = SolutionCreateForm(
            data={
                "problem": self.problem.id,
                "language": self.language.id,
                "source_code": "def solve(): pass",
                "test_cases": "(solve(), None)",
                "time_complexity": time_complexity.id,
                "space_complexity": space_complexity.id,
                "order": 1,
            }
        )
        self.assertTrue(form.is_valid())
        solution = form.save(commit=False)
        solution.owner = self.owner
        solution.save()
        self.assertEqual(solution.problem, self.problem)
        self.assertEqual(solution.language, self.language)
        self.assertEqual(solution.source_code, "def solve(): pass")

    def test_solution_update_form_valid_data(self):
        from .forms import SolutionUpdateForm
        solution = create_sample_solution(
            problem=self.problem, language=self.language, owner=self.owner
        )
        time_complexity = Complexity.objects.get_or_create(name="O(n)")[0]
        space_complexity = Complexity.objects.get_or_create(name="O(n)")[0]
        form = SolutionUpdateForm(
            instance=solution,
            data={
                "source_code": "def solve(): return 42",
                "time_complexity": time_complexity.id,
                "space_complexity": space_complexity.id,
                "order": 2,
            },
        )
        self.assertTrue(form.is_valid())
        updated = form.save()
        self.assertEqual(updated.source_code, "def solve(): return 42")
        self.assertEqual(updated.order, 2)

    def test_solution_create_form_requires_problem_and_language(self):
        from .forms import SolutionCreateForm
        form = SolutionCreateForm(
            data={
                "source_code": "def solve(): pass",
                "test_cases": "(solve(), None)",
                "order": 1,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("problem", form.errors)
        self.assertIn("language", form.errors)
