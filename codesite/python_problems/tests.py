from django.test import TestCase
from django.urls import reverse

from .models import Problem, Difficulty, Complexity


def create_sample_problem(title="Two Sum", difficulty_name="Easy", time_complexity_name="O(n)", space_complexity_name="O(n)"):
    """
    Create a problem sample for other tests.
    """
    difficulty, _ = Difficulty.objects.get_or_create(name=difficulty_name)
    time_complexity, _ = Complexity.objects.get_or_create(
        name=time_complexity_name)
    space_complexity, _ = Complexity.objects.get_or_create(
        name=space_complexity_name)

    return Problem.objects.create(title=title, difficulty=difficulty, time_complexity=time_complexity, space_complexity=space_complexity)


class ProblemModelTests(TestCase):

    def test_create_difficulty(self):
        """
        Test creating a Difficulty instance.
        """
        difficulty_1 = Difficulty.objects.create(name="Medium")
        Difficulty.objects.create(name="Easy")
        difficulties = Difficulty.objects.all()

        self.assertEqual(difficulty_1.name, "Medium")
        self.assertEqual(difficulties[1].name, "Easy")
        self.assertEqual(Difficulty.objects.count(), 2)

    def test_create_sample_problem(self):
        """
        Test creating a Problem instance linked to a Difficulty instance.
        """
        problem = create_sample_problem(
            title="Two Sum", difficulty_name="Easy", time_complexity_name="O(n)", space_complexity_name="O(n)")
        self.assertEqual(problem.title, "Two Sum")
        self.assertEqual(problem.difficulty.name, "Easy")
        self.assertEqual(problem.time_complexity.name, "O(n)")
        self.assertEqual(problem.space_complexity.name, "O(n)")
        self.assertEqual(Problem.objects.count(), 1)
        self.assertEqual(Difficulty.objects.count(), 1)

    def test_create_two_problems_with_same_difficulty(self):
        """
        Test creating two Problem instances linked to the same Difficulty instance.
        """
        create_sample_problem(title="Two Sum")
        create_sample_problem(title="Valid Parentheses",
                              difficulty_name="Easy")
        problems = Problem.objects.all()
        self.assertEqual(problems.count(), 2)
        self.assertEqual(Difficulty.objects.count(), 1)
        self.assertEqual(problems[0].difficulty, problems[1].difficulty)

    def test_create_two_problems_with_different_difficulties(self):
        """
        Test creating two Problem instances linked to different Difficulty instances.
        """
        create_sample_problem(title="Two Sum")
        create_sample_problem(
            title="Two Sum II - Input Array Is Sorted", difficulty_name="Medium")
        problems = Problem.objects.all()
        self.assertEqual(problems.count(), 2)
        self.assertEqual(Difficulty.objects.count(), 2)
        self.assertNotEqual(problems[0].difficulty, problems[1].difficulty)


class ProblemIndexViewTests(TestCase):
    def test_no_problems(self):
        """
        If no problems exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("python_problems:index"))
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
        response = self.client.get(reverse("python_problems:index"))
        self.assertTemplateUsed(response, "python_problems/problem_list.html")

    def test_with_problem(self):
        """
        If problem exists, it is displayed on the index page.
        """
        title = "Two Sum"
        create_sample_problem(title=title)
        response = self.client.get(reverse("python_problems:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, title)
        self.assertQuerySetEqual(
            response.context["problem_list"],
            Problem.objects.all()
        )
        self.assertEqual(Problem.objects.count(), 1)
        self.assertEqual(response.context["problem_list"].count(), 1)

    def test_with_problems(self):
        """
        If problems exist, they are displayed on the index page.
        """
        create_sample_problem(title="Two Sum")
        create_sample_problem(
            title="Two Sum II - Input Array Is Sorted", difficulty_name="Medium")
        problems = Problem.objects.all()
        response = self.client.get(reverse("python_problems:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Two Sum")
        self.assertContains(response, "Two Sum II - Input Array Is Sorted")

        self.assertEqual(Problem.objects.count(), 2)
        self.assertEqual(response.context["problem_list"].count(), 2)

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


class ProblemDetailViewTests(TestCase):
    def test_right_template(self):
        """
        Test if the right template is choosen.
        """
        problem = create_sample_problem(title="Two Sum")
        response = self.client.get(
            reverse("python_problems:detail", kwargs={"slug": problem.slug}))
        self.assertTemplateUsed(
            response, "python_problems/problem_detail.html")

    def test_context_data(self):
        """
        Test if the correct context data is passed to the template.
        """
        problem = create_sample_problem(
            title="Two Sum", difficulty_name="Easy")
        response = self.client.get(
            reverse("python_problems:detail", kwargs={"slug": problem.slug}))
        self.assertEqual(response.context["problem"], problem)

    def test_404_response(self):
        """
        Test if a 404 response is returned for a non-existent problem.
        """
        response = self.client.get(
            reverse("python_problems:detail", kwargs={"slug": "non-existent-slug"}))
        self.assertEqual(response.status_code, 404)
    
    def test_problem_details_display(self):
        """
        Test if the problem details are correctly displayed in the template.
        """
        problem = create_sample_problem(
            title="Two Sum", difficulty_name="Easy")
        response = self.client.get(
            reverse("python_problems:detail", kwargs={"slug": problem.slug}))

        self.assertContains(response, problem.title)
        self.assertContains(response, problem.difficulty.name)
