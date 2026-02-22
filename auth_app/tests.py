from django.test import TestCase
from rest_framework.test import APIClient

class AuthProtectedRoutesTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_profile_requires_auth_returns_401(self):
        """
        Requirement: protected route must return 401 without JWT.
        """
        res = self.client.get("/api/profile/")
        self.assertEqual(res.status_code, 401)