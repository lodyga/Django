import html
import json

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
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
    TestCase as ProblemTestCase,
)
from .scripts import (
    build_problem_test_case_expression,
    build_validation_class_payload,
    build_validation_in_place_payload,
    get_ui_test_cases,
    draw_linked_list,
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
        problem.argument_names = ["nums", "target"]
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
                "difficulty": difficulty.id,
                "description": "Sample problem description",
                "tags": [tag.id],
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
                "difficulty": difficulty.id,
                "description": "Sample problem description",
                "tags": [tag.id],
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
                "difficulty": difficulty.id,
                "description": "Sample problem description",
                "tags": [tag.id],
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
                "difficulty": difficulty.id,
                "description": "Detect a cycle in a linked list.",
                "tags": [tag.id],
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
        updated_code, expected_output = build_validation_in_place_payload(
            source_code,
            "Python",
            problem.testcases,
            "moveZeroes",
        )

        self.assertIn("\nsolution = Solution()\n", updated_code)
        self.assertIn("inputs_list = [[[0, 1, 0, 3, 12]]]", updated_code)
        self.assertIn("run_tests(solution.moveZeroes)", updated_code)
        self.assertEqual(expected_output, ["[[1, 3, 12, 0, 0]]"])

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

        ui_test_cases = get_ui_test_cases(problem, solution, "Python")

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
        updated_code, expected_output = build_validation_class_payload(
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
        self.assertEqual(
            expected_output,
            ["[None, None, 'bar', 'bar', None, 'bar2', 'bar2']"],
        )

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
            "serialize_tree(solution.invertTree(build_tree([4, 2, 7, 1, 3, 6, 9])))",
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


class TestCaseCrudViewTests(TestCase):
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
            response.context["effective_test_cases"],
            [("solution.twoSum([2, 7, 11, 15], 9)", "[0, 1]")],
        )

    def test_problem_argument_names_label_ui_testcases(self):
        problem = create_sample_problem()
        problem.method_name = "twoSum"
        problem.argument_names = ["nums", "target"]
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

        ui_test_case = response.context["ui_test_cases"][0]
        self.assertEqual(ui_test_case["input"], "nums = [2, 7, 11, 15]\ntarget = 9")
        self.assertEqual(
            response.context["clipboard_test_cases"],
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
