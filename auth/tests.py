from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse


class AuthTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )

        self.login_url = reverse("auth:auth_login")
        self.logout_url = reverse("auth:auth_logout")

    def test_login_success(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpass123"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tokens", response.data)
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])
        self.assertIn("user", response.data)

    def test_login_failure(self):
        response = self.client.post(
            self.login_url,
            {"username": "testuser", "password": "wrongpassword"},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_success(self):
        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        response = self.client.post(
            self.logout_url, {"refresh_token": str(refresh)}
        )

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(response.data["detail"], "logged out")

    def test_logout_without_token(self):
        response = self.client.post(
            self.logout_url, {"refresh_token": "invalid_token"}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
