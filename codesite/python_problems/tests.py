from .models import Complexity, Difficulty, Language, Problem, Solution, Tag
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
import django
import html
import os

# Update with your project name
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
        Language.objects.all().delete()
        create_sample_solution(
            language=Language.objects.get_or_create(name="Python")[0]
        )
        create_sample_solution(
            language=Language.objects.get_or_create(name="JavaScript")[0]
        )
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
        create_sample_solution(
            create_sample_problem(
                title="Valid Parentheses"
            )
        )
        solutions = Solution.objects.all()
        self.assertEqual(solutions.count(), 2)
        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(solutions[0].language, solutions[1].language)


class ProblemIndexViewTests(TestCase):
    def test_no_problems(self):
        """
        If no problems exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("python_problems:problem-index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No python problems available.")
        # Same as assertContains, but with manual content.decode()
        self.assertIn("No python problems available.",
                      response.content.decode())
        self.assertQuerySetEqual(response.context["problem_list"], [])

    def test_right_template(self):
        """
        Test if the right template is choosen.
        """
        template_name = "python_problems/problem_list.html"
        response = self.client.get(reverse("python_problems:problem-index"))
        self.assertTemplateUsed(response, template_name)
        self.assertListEqual(response.template_name, [template_name])

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
        solution = create_sample_solution(
            problem=create_sample_problem(
                title="Two Sum"
            ),
            language=Language.objects.get_or_create(name="Python")[0]
        )
        url = reverse(
            "python_problems:problem-detail",
            kwargs={"slug": solution.problem.slug,
                    "language": solution.language.name})
        response = self.client.get(url)
        self.assertTemplateUsed(
            response, "python_problems/problem_detail.html")

    def test_context_data(self):
        """
        Test if the correct context data is passed to the template.
        """
        solution = create_sample_solution()
        url = reverse(
            "python_problems:problem-detail",
            kwargs={"slug": solution.problem.slug,
                    "language": solution.language.name})
        response = self.client.get(url)
        self.assertEqual(
            response.context["problem"].problem_solutions.first(), solution)

    def test_404_response(self):
        """
        Test if a 404 response is returned for a non-existent problem.
        """
        url = reverse(
            "python_problems:problem-detail",
            kwargs={"slug": "non-existent-slug",
                    "language": "non-existent-language"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_problem_details_display(self):
        """
        Test if the problem details are correctly displayed in the template.
        """
        User = get_user_model()
        solution = create_sample_solution(
            problem=create_sample_problem(
                title="Two Sum",
                owner=User.objects.get_or_create(
                    username="tester", password="testpass")[0]
            ),
            language=Language.objects.get_or_create(name="Python")[0],
            owner=User.objects.get_or_create(
                username="tester", password="testpass")[0]
        )
        url = reverse(
            "python_problems:problem-detail",
            kwargs={"slug": solution.problem.slug,
                    "language": solution.language.name})
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
        url = reverse(
            "python_problems:problem-detail",
            kwargs={"slug": self.problem.slug,
                    "language": self.language_1.name})

        response = self.client.get(url)
        content = html.unescape(response.content.decode())

        # Verify response contains the correct solution before the update
        self.assertIn(self.solution_text_1, content)
        # Verify the final URL includes the correct language
        self.assertEqual(
            response.request["PATH_INFO"], f"/python/{self.problem.slug}/{self.language_1.name}/")

        # Simulate changing the language via POST
        response = self.client.post(
            url, {"language": self.language_2.id}, follow=True)

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
            owner=self.owner_1
        )
        self.solution_2 = create_sample_solution(
            problem=self.problem,
            language=self.language,
            solution=self.solution_text_2,
            owner=self.owner_2
        )

    def test_switching_owner_updates_solution(self):
        """
        Check if selecting a different owner updates the displayed solution.
        """
        url = reverse(
            "python_problems:problem-detail",
            kwargs={"slug": self.problem.slug,
                    "language": self.language.name})

        response = self.client.get(url)
        content = html.unescape(response.content.decode())

        # Verify response contains the correct solution before the update
        self.assertIn(self.solution_text_1, content)

        # Simulate changing the user via POST
        response = self.client.post(
            url, {"owner": self.owner_2.id}, follow=True)

        # Decode HTML entities in response content
        content = html.unescape(response.content.decode())

        # Verify response contains the correct solution after the update
        self.assertIn(self.solution_text_2, content)
