from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


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
