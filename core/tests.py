from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
import os
from python_problems.models import Language
from core.scripts import (
    test_cohere_connection,
    test_gemini_connection,
    test_mistral_connection,
)


class HomepageTests(TestCase):
    def test_homepage_lists_the_requested_problem_languages_in_order(self):
        language_names = [
            "Pandas",
            "Java",
            "C++",
            "Python",
            "JavaScript",
        ]
        for name in language_names:
            Language.objects.get_or_create(name=name)

        response = self.client.get(reverse("core:index"))

        self.assertEqual(
            [language.name for language in response.context["languages"]],
            ["Python", "JavaScript", "C++", "Java"],
        )
        problem_index_url = reverse("python_problems:problem-index")
        for language in response.context["languages"]:
            self.assertContains(
                response,
                f'href="{problem_index_url}?language_id={language.id}"',
            )
        self.assertNotContains(response, "Pandas")


class LogoutRedirectTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="logout-user", password="test-password"
        )
        self.client.force_login(self.user)

    def test_header_logout_redirects_to_current_path(self):
        current_path = f"{reverse('core:contact')}?source=navbar"

        response = self.client.get(current_path)

        self.assertContains(
            response,
            f'<input type="hidden" name="next" value="{current_path}">',
            count=2,
        )

        response = self.client.post(reverse("logout"), {"next": current_path})

        self.assertRedirects(response, current_path, fetch_redirect_response=False)


class AIProviderConnectionTests(TestCase):
    def test_cohere_connection(self):
        if not os.getenv("COHERE_API_KEY"):
            self.skipTest("COHERE_API_KEY is not configured")
        ok, message = test_cohere_connection()
        self.assertTrue(ok, message)

    def test_gemini_connection(self):
        if not os.getenv("GEMINI_API_KEY"):
            self.skipTest("GEMINI_API_KEY is not configured")
        ok, message = test_gemini_connection()
        self.assertTrue(ok, message)

    def test_mistral_connection(self):
        if not os.getenv("MISTRAL_API_KEY"):
            self.skipTest("MISTRAL_API_KEY is not configured")
        ok, message = test_mistral_connection()
        self.assertTrue(ok, message)
