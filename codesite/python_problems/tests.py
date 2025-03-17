import django
import html
import os
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse
from .models import Complexity, Difficulty, Language, Problem, Solution, Tag
from .views import ProblemIndexView


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codesite.settings")
django.setup()  # Initialize Django


def create_sample_problem(
        title=None,
        tags=None,
        difficulty=None,
        url=None,
        description=None,
        owner=None):
    """
    Create a problem sample for other tests.
    """
    User = get_user_model()
    if title is None:
        title = "Two Sum"
    if tags is None:
        tags = [Tag.objects.get_or_create(name="Array")[0]]
    if difficulty is None:
        difficulty, _ = Difficulty.objects.get_or_create(name="Easy")
    if url is None:
        url = "https://example.com"
    if description is None:
        description = "Sample problem description"
    if owner is None:
        owner, _ = User.objects.get_or_create(
            username="tester", password="testpass")

    problem, problem_created = Problem.objects.get_or_create(
        title=title,
        difficulty=difficulty,
        url=url,
        description=description,
        owner=owner
    )
    if problem_created:
        problem.tags.set(tags)

    return problem


def create_sample_solution(
        problem=None,
        language=None,
        owner=None,
        solution=None,
        testcase=None,
        time_complexity=None,
        space_complexity=None):
    """
    Create a solution sample for other tests.
    """
    User = get_user_model()
    if problem is None:
        problem = create_sample_problem()
    if language is None:
        language, _ = Language.objects.get_or_create(name="Python")
    if owner is None:
        owner, _ = User.objects.get_or_create(
            username="tester", password="testpass")
    if solution is None:
        solution = "Simple solution."
    if testcase is None:
        testcase = "Simple testcase."
    if time_complexity is None:
        time_complexity, _ = Complexity.objects.get_or_create(name="O(n)")
    if space_complexity is None:
        space_complexity, _ = Complexity.objects.get_or_create(name="O(n)")

    solution = Solution.objects.create(
        problem=problem,
        language=language,
        owner=owner,
        solution=solution,
        testcase=testcase,
        time_complexity=time_complexity,
        space_complexity=space_complexity
    )
    return solution


class BasicModelTests(TestCase):
    def test_create_tag(self):
        """
        Test creating a Tag instance.
        """
        Tag.objects.create(name="Array")
        tags = Tag.objects.all()
        self.assertEqual(tags[0].name, "Array")
        self.assertEqual(Tag.objects.count(), 1)

    def test_create_difficulty(self):
        """
        Test creating a Difficulty instance.
        """
        Difficulty.objects.create(name="Easy")
        difficulties = Difficulty.objects.all()
        self.assertEqual(difficulties[0].name, "Easy")
        self.assertEqual(Difficulty.objects.count(), 1)

    def test_create_complexity(self):
        """
        Test creating a Complexity instance.
        """
        Complexity.objects.create(name="O(1)")
        complexities = Complexity.objects.all()
        self.assertEqual(complexities[0].name, "O(1)")
        self.assertEqual(Complexity.objects.count(), 1)

    def test_create_language(self):
        """
        Test creating a Language instance.
        """
        # Becaouse of 0021_populate_language.py
        # which creates Python and JavaScript languages
        # delete all languages
        Language.objects.all().delete()
        Language.objects.create(name="Python")
        languages = Language.objects.all()
        self.assertEqual(languages[0].name, "Python")
        self.assertEqual(Language.objects.count(), 1)


class ProblemModelTests(TestCase):
    def test_create_sample_problem(self):
        """
        Test creating a Problem instance linked to a Difficulty instance.
        """
        User = get_user_model()
        title = "Two Sum"
        tags = [
            Tag.objects.create(name="Array"),
            Tag.objects.create(name="Hash Table")
        ]
        difficulty = Difficulty.objects.create(name="Easy")
        url = "https://example.com"
        description = "Sample problem description"
        owner, _ = User.objects.get_or_create(
            username="tester", password="testpass")
        problem = create_sample_problem(
            title,
            tags,
            difficulty,
            url,
            description,
            owner=owner
        )
        self.assertEqual(problem.title, title)
        self.assertIn(tags[0], problem.tags.all())
        self.assertIn(tags[1], problem.tags.all())
        self.assertEqual(problem.difficulty, difficulty)
        self.assertEqual(problem.url, url)
        self.assertEqual(problem.description, description)
        self.assertEqual(problem.owner, owner)

    def test_create_two_problems_with_same_difficulty(self):
        """
        Test creating two Problem instances linked to the same Difficulty instance.
        """
        create_sample_problem(
            title="Two Sum",
            difficulty=Difficulty.objects.get_or_create(name="Easy")[0]
        )
        create_sample_problem(
            title="Valid Parentheses",
            difficulty=Difficulty.objects.get_or_create(name="Easy")[0]
        )
        problems = Problem.objects.all()
        self.assertEqual(Problem.objects.count(), 2)
        self.assertEqual(Difficulty.objects.count(), 1)
        self.assertEqual(problems[0].difficulty, problems[1].difficulty)

    def test_create_two_problems_with_different_difficulties(self):
        """
        Test creating two Problem instances linked to different Difficulty instances.
        """
        create_sample_problem(
            title="Two Sum",
            difficulty=Difficulty.objects.get_or_create(name="Easy")[0]
        )
        create_sample_problem(
            title="Two Sum II - Input Array Is Sorted",
            difficulty=Difficulty.objects.get_or_create(name="Medium")[0]
        )
        problems = Problem.objects.all()
        self.assertEqual(problems.count(), 2)
        self.assertEqual(Difficulty.objects.count(), 2)
        self.assertNotEqual(problems[0].difficulty, problems[1].difficulty)


class SolutionModelTests(TestCase):
    def test_create_sample_solution(self):
        """
        Test creating a Solution instance linked to a Problem instance.
        """
        User = get_user_model()
        problem = create_sample_problem()
        Language.objects.all().delete()
        language = Language.objects.create(name="Python")
        owner, _ = User.objects.get_or_create(
            username="tester", password="testpass")
        solution_text = "Simple solution."
        testcase = "Simple testcase."
        time_complexity, _ = Complexity.objects.get_or_create(name="O(n)")
        space_complexity, _ = Complexity.objects.get_or_create(name="O(n)")

        solution = create_sample_solution(
            problem=problem,
            language=language,
            owner=owner,
            solution=solution_text,
            testcase=testcase,
            time_complexity=time_complexity,
            space_complexity=space_complexity
        )

        self.assertEqual(solution.problem, problem)
        self.assertEqual(solution.language, language)
        self.assertEqual(solution.owner, owner)
        self.assertEqual(solution.solution, solution_text)
        self.assertEqual(solution.testcase, testcase)
        self.assertEqual(solution.time_complexity, time_complexity)
        self.assertEqual(solution.space_complexity, space_complexity)

    def test_create_two_solutions_in_different_languages_for_same_problem(self):
        """
        Test creating two Solution instances in different Language instances
        linked to the same Problem instance.
        """
        # Language.objects.all().delete()
        language_1, _ = Language.objects.get_or_create(name="Python")
        language_2, _ = Language.objects.get_or_create(name="JavaScript")
        create_sample_solution(language=language_1)
        create_sample_solution(language=language_2)
        solutions = Solution.objects.all()
        self.assertEqual(solutions.count(), 2)
        self.assertEqual(Language.objects.count(), 2)
        self.assertNotEqual(solutions[0].language, solutions[1].language)

    def test_create_two_solutions_in_same_language_for_different_problems(self):
        """
        Test creating two Solution instances in the same Language instance
        linked to different Problem instances.
        """
        Language.objects.all().delete()
        create_sample_solution()
        title = "Valid Parentheses"
        problem = create_sample_problem(title=title)
        create_sample_solution(problem=problem)
        solutions = Solution.objects.all()
        self.assertEqual(solutions.count(), 2)
        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(solutions[0].language, solutions[1].language)


class ProblemIndexViewTests0(TestCase):
    def test_no_problems(self):
        """
        If no problems exist, an appropriate message is displayed.
        """
        viewname = "python_problems:problem-index"
        url = reverse(viewname)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "No Python problems available for the given parameters.")
        # Same as assertContains, but with manual content.decode()
        self.assertIn("No Python problems available for the given parameters.",
                      response.content.decode())
        self.assertQuerySetEqual(response.context["problem_list"], [])

    def test_right_template(self):
        """
        Test if the right template is choosen.
        """
        template_name = "python_problems/problem_list.html"
        viewname = "python_problems:problem-index"
        url = reverse(viewname)
        response = self.client.get(url)
        self.assertTemplateUsed(response, template_name)

    def test_with_problem(self):
        """
        If problem exists, it is displayed on the index page.
        """
        title = "Two Sum"
        create_sample_problem(title=title)
        response = self.client.get(reverse("python_problems:problem-index"))
        self.assertContains(response, title)
        self.assertQuerySetEqual(
            response.context["problem_list"], Problem.objects.all())
        self.assertEqual(
            response.context["problem_list"].count(), Problem.objects.count())

    def test_with_problems(self):
        """
        If problems exist, they are displayed on the index page.
        """
        create_sample_problem(title="Two Sum")
        create_sample_problem(title="Valid Parentheses")
        response = self.client.get(reverse("python_problems:problem-index"))
        self.assertContains(response, "Two Sum")
        self.assertContains(response, "Valid Parentheses")
        self.assertEqual(
            response.context["problem_list"].count(), Problem.objects.count())

        # Ensure both querysets are ordered
        expected_queryset = Problem.objects.all().order_by("id")
        actual_queryset = response.context["problem_list"].order_by("id")

        # QuerySets comprare based on ordered QuerySets
        self.assertQuerySetEqual(actual_queryset, expected_queryset)

        # Compare QuerySets entities based on elements id's.
        self.assertEqual(Problem.objects.all().get(
            id=1), response.context["problem_list"].get(id=1))
        self.assertEqual(Problem.objects.all().get(
            id=2), response.context["problem_list"].get(id=2))


class SolutionDetailViewTests(TestCase):
    def test_right_template(self):
        """
        Test if the right template is choosen.
        """
        template_name = "python_problems/problem_detail.html"
        solution = create_sample_solution()
        viewname = "python_problems:problem-detail"
        kwargs = {"slug": solution.problem.slug,
                  "language": solution.language.name}
        url = reverse(viewname, kwargs=kwargs)
        response = self.client.get(url)
        self.assertTemplateUsed(response, template_name)

    def test_context_data(self):
        """
        Test if the correct context data is passed to the template.
        """
        solution = create_sample_solution()
        viewname = "python_problems:problem-detail"
        kwargs = {"slug": solution.problem.slug,
                  "language": solution.language.name}
        url = reverse(viewname, kwargs=kwargs)
        response = self.client.get(url)
        actual_solution = response.context["problem"].problem_solutions.first()
        self.assertEqual(actual_solution, solution)

    def test_404_response(self):
        """
        Test if a 404 response is returned for a non-existent problem.
        """
        status_code = 404
        viewname = "python_problems:problem-detail"
        kwargs = {"slug": "non-existent-slug",
                  "language": "non-existent-language"}
        url = reverse(viewname, kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)

    def test_problem_details_display(self):
        """
        Test if the problem details are correctly displayed in the template.
        """
        User = get_user_model()
        title = "Two Sum"
        owner, _ = User.objects.get_or_create(
            username="tester", password="testpass")
        language, _ = Language.objects.get_or_create(name="Python")
        problem = create_sample_problem(
            title=title,
            owner=owner)
        solution = create_sample_solution(
            problem=problem,
            language=language,
            owner=owner)
        viewname = "python_problems:problem-detail"
        kwargs = {"slug": solution.problem.slug,
                  "language": solution.language.name}
        url = reverse(viewname, kwargs=kwargs)
        response = self.client.get(url)

        self.assertContains(response, solution.problem.title)
        self.assertContains(response, solution.problem.owner)
        self.assertContains(response, solution.language)
        self.assertContains(response, solution.owner)


class SolutionLanguageSwitchTest(TestCase):
    def setUp(self):
        """
        Set up test data.
        """
        Language.objects.all().delete()
        self.language_1, _ = Language.objects.get_or_create(name="Python")
        self.language_2, _ = Language.objects.get_or_create(name="JavaScript")
        self.solution_text_1 = "print('Python solution')"
        self.solution_text_2 = "console.log('JavaScript solution');"
        self.problem = create_sample_problem()
        self.solution_1 = create_sample_solution(
            problem=self.problem,
            language=self.language_1,
            solution=self.solution_text_1
        )
        self.solution_2 = create_sample_solution(
            problem=self.problem,
            language=self.language_2,
            solution=self.solution_text_2
        )

    def test_switching_language_updates_solution(self):
        """
        Check if selecting a different language updates the displayed solution.
        """
        viewname = "python_problems:problem-detail"
        kwargs = {"slug": self.problem.slug,
                  "language": self.language_1.name}
        url = reverse(viewname, kwargs=kwargs)
        response = self.client.get(url)
        content = html.unescape(response.content.decode())

        # Verify response contains the correct solution before the update
        self.assertIn(self.solution_text_1, content)
        # Verify the final URL includes the correct language
        self.assertEqual(
            response.request["PATH_INFO"], f"/python/{self.problem.slug}/{self.language_1.name}/")

        # Simulate changing the language via POST
        response = self.client.post(
            url,
            {"language": self.language_2.id},
            follow=True)

        # Decode HTML entities in response content
        content = html.unescape(response.content.decode())

        # Verify response contains the correct solution after the update
        self.assertIn(self.solution_text_2, content)

        self.assertEqual(
            response.request["PATH_INFO"], f"/python/{self.problem.slug}/{self.language_2.name}/")


class SolutionUserSwitchTest(TestCase):
    def setUp(self):
        """
        Set up test data.
        """
        Language.objects.all().delete()
        User = get_user_model()
        self.language, _ = Language.objects.get_or_create(name="Python")
        self.solution_text_1 = "print('Python solution')"
        self.solution_text_2 = "print('Python solution 2')"
        self.owner_1, _ = User.objects.get_or_create()
        self.owner_2, _ = User.objects.get_or_create(
            username="tester_2", password="testpass")
        self.problem = create_sample_problem()
        self.solution_1 = create_sample_solution(
            problem=self.problem,
            language=self.language,
            solution=self.solution_text_1,
            owner=self.owner_1)
        self.solution_2 = create_sample_solution(
            problem=self.problem,
            language=self.language,
            solution=self.solution_text_2,
            owner=self.owner_2)

    def test_switching_owner_updates_solution(self):
        """
        Check if selecting a different owner updates the displayed solution.
        """
        viewname = "python_problems:problem-detail"
        kwargs = {"slug": self.problem.slug,
                  "language": self.language.name}
        url = reverse(viewname, kwargs=kwargs)
        response = self.client.get(url)
        content = html.unescape(response.content.decode())

        # Verify response contains the correct solution before the update
        self.assertIn(self.solution_text_1, content)

        # Simulate changing the user via POST
        response = self.client.post(
            url,
            {"owner_id": self.owner_2.id},
            follow=True)

        # Decode HTML entities in response content
        content = html.unescape(response.content.decode())

        # Verify response contains the correct solution after the update
        self.assertIn(self.solution_text_2, content)


class ProblemIndexViewTests1(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        Language.objects.all().delete()
        cls.difficulty_easy = Difficulty.objects.create(name="Easy")
        cls.difficulty_medium = Difficulty.objects.create(name="Medium")

        cls.tag_array, _ = Tag.objects.get_or_create(name="Array")
        cls.tag_two_pointers, _ = Tag.objects.get_or_create(
            name="Two Pointers")

        cls.language_python, _ = Language.objects.get_or_create(name="Python")
        cls.language_javaScript, _ = Language.objects.get_or_create(
            name="JavaScript")

        # Create multiple problems
        cls.problem_easy = create_sample_problem(
            title="Two Sum",
            difficulty=cls.difficulty_easy,
            tags=[cls.tag_array])
        cls.problem_medium = create_sample_problem(
            title="Two Sum II - Input Array Is Sorted",
            difficulty=cls.difficulty_medium,
            tags=[cls.tag_array, cls.tag_two_pointers])

        # Create solutions
        create_sample_solution(
            problem=cls.problem_easy,
            language=cls.language_python,
            solution="print('Easy')")
        create_sample_solution(
            problem=cls.problem_medium,
            language=cls.language_javaScript,
            solution="System.out.println('Medium')")

    def test_filter_by_difficulty(self):
        """
        Test filtering by difficulty_id.
        """
        url = reverse("python_problems:problem-index")
        response = self.client.post(
            url,
            {"difficulty_id": self.difficulty_easy.id},
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Two Sum")
        self.assertNotContains(response, "Two Sum II - Input Array Is Sorted")

    def test_filter_by_tag(self):
        """
        Test filtering by tag_id.
        """
        url = reverse("python_problems:problem-index")
        response = self.client.post(
            url,
            {"tag_id": self.tag_two_pointers.id},
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Two Sum II - Input Array Is Sorted")

    def test_search_by_query_text(self):
        """
        Test filtering by query_text (title and tag names).
        """
        url = reverse("python_problems:problem-index")
        response = self.client.post(
            url,
            {"query_text": "Sorted"},
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Two Sum II - Input Array Is Sorted")

    def test_ordering(self):
        """
        Test ordering by 'title'.
        """
        url = reverse("python_problems:problem-index")
        response = self.client.post(
            url,
            {"order_by": "title"},
            follow=True)
        self.assertEqual(response.status_code, 200)
        problems = list(response.context["problem_list"])
        sorted_problems = sorted(
            response.context["problem_list"],
            key=lambda problem: problem.title)
        self.assertEqual(problems, sorted_problems)

    def test_pagination(self):
        """
        Test pagination with multiple problems per page.
        """
        for index in range(15):
            create_sample_problem(title=f"Problem {index}")

        url = reverse("python_problems:problem-index")
        response = self.client.post(
            url,
            {"problems_per_page": 5,
             "page_number": 2},
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(response.context["page_obj"].paginator.per_page, 5)

    def test_preserve_all_filters(self):
        """
        Test that all filters persist together.
        """
        url = reverse("python_problems:problem-index")
        response = self.client.post(
            url,
            {"difficulty_id": self.difficulty_easy.id,
             "tag_id": self.tag_array.id,
             "query_text": "Problem",
             "order_by": "title",
             "problems_per_page": 5,
             "page_number": 1},
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["difficulty_id"], self.difficulty_easy.id)
        self.assertEqual(response.context["tag_id"], self.tag_array.id)
        self.assertEqual(response.context["query_text"], "Problem")
        self.assertEqual(response.context["order_by"], "title")
        self.assertEqual(response.context["problems_per_page"], 5)
        self.assertEqual(response.context["page_obj"].number, 1)


class ProblemIndexViewTests2(TestCase):
    def setUp(self):
        # Create test data
        self.factory = RequestFactory()
        User = get_user_model()
        self.user, _ = User.objects.get_or_create(
            username="tester", password="testpass")

        # Create languages
        Language.objects.all().delete()
        self.language_python, _ = Language.objects.get_or_create(name="Python")
        self.language_javaScript, _ = Language.objects.get_or_create(
            name="JavaScript")

        # Create difficulties
        self.difficulty_easy, _ = Difficulty.objects.get_or_create(name="Easy")
        self.difficulty_medium, _ = Difficulty.objects.get_or_create(
            name="Medium")

        # Create tags
        self.tag_array = Tag.objects.create(name="Array")
        self.tag_two_pointers = Tag.objects.create(name="Two Pointers")

        # Create problems
        self.problem_1 = create_sample_problem(
            title="Two Sum",
            difficulty=self.difficulty_easy,
            description="Description 1")
        self.problem_1.tags.add(self.tag_array)

        self.problem_2 = create_sample_problem(
            title="Two Sum II - Input Array Is Sorted",
            difficulty=self.difficulty_medium,
            description="Description 2")
        self.problem_2.tags.add(self.tag_two_pointers)

        # Create solutions
        create_sample_solution(
            problem=self.problem_1,
            language=self.language_python,
            solution="Solution 1",
            owner=self.user
        )
        create_sample_solution(
            problem=self.problem_2,
            language=self.language_javaScript,
            solution="Solution 2",
            owner=self.user
        )

    def test_get_request(self):
        # Create a GET request
        url = reverse("python_problems:problem-index")
        request = self.factory.get(url)
        request.user = self.user

        # Call the view
        response = ProblemIndexView.as_view()(request)

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Check the context data
        self.assertIn("difficulty_id", response.context_data)
        self.assertIn("order_by", response.context_data)
        self.assertIn("page_obj", response.context_data)
        self.assertIn("problem_list", response.context_data)
        self.assertIn("problems_per_page", response.context_data)
        self.assertIn("query_text", response.context_data)
        self.assertIn("tag_id", response.context_data)

        # Verify initial values
        self.assertEqual(response.context_data["difficulty_id"], 0)
        self.assertEqual(response.context_data["order_by"], "created_at")
        self.assertEqual(response.context_data["problems_per_page"], 7)
        self.assertEqual(response.context_data["query_text"], "")
        self.assertEqual(response.context_data["tag_id"], 0)

        # Verify problem list
        self.assertQuerysetEqual(
            response.context_data["problem_list"].order_by('id'),
            Problem.objects.all().order_by('id'),
            # Compare objects directly (no transformation)
            transform=lambda x: x)