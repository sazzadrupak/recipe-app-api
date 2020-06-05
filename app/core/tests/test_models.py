from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@recipe.com"
        password = "ZAQ!2wsx"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test a new user email is normalized"""
        email = "test@RECIPE.com"
        user = get_user_model().objects.create_user(
            email, "ZAQ!2wsx"
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_email_invalid(self):
        """Test a new user email is invalid and raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test1234")

    def test_create_super_user(self):
        """Test create a super user"""
        user = get_user_model().objects.create_super_user(
            'test@recipe.com',
            'test1234'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
