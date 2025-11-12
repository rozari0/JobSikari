import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="super@user.com", password="foo"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False
            )


class RegistrationApiTests(TestCase):
    def test_register_requires_fullname_and_valid_email_and_password(self):
        client = self.client

        # Missing fullname -> schema validation (422)
        resp = client.post(
            "/api/register",
            data=json.dumps({"email": "a@example.com", "password": "longenough"}),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 422)

        # Invalid email -> handled by view validation -> 400 or schema 422
        resp = client.post(
            "/api/register",
            data=json.dumps(
                {
                    "fullname": "Alice",
                    "email": "not-an-email",
                    "password": "longenough",
                }
            ),
            content_type="application/json",
        )
        # Ninja/Pydantic may return 422 for type/format issues; accept 400 or 422
        self.assertIn(resp.status_code, (400, 422))

        # Short password -> our view returns 400
        resp = client.post(
            "/api/register",
            data=json.dumps(
                {
                    "fullname": "Alice",
                    "email": "a@example.com",
                    "password": "short",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 400)

        # Successful registration
        resp = client.post(
            "/api/register",
            data=json.dumps(
                {
                    "fullname": "Alice",
                    "email": "a@example.com",
                    "password": "longenough",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        body = resp.json()
        self.assertIn("email", body)
        self.assertEqual(body["email"], "a@example.com")
