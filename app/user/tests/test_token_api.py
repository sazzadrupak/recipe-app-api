from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class TokenApiTest(TestCase):
    """Test the token API"""
    def setUp(self):
        self.client = APIClient()

    def test_create_token_for_user(self):
        """Test create token for a valid user"""
        payload = {
            'email': 'test@recipe.com',
            'password': 'ZAQ!2wsx',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_with_invalid_credentials(self):
        """Test create token with invalid credentials"""
        payload = {
            'email': 'test@recipe.com',
            'password': 'ZAQ!2wsx',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL,
                               {
                                   'email': 'test@recipe.com',
                                   'password': 'wrong'
                               })
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_non_exists_user(self):
        """Test create token for a non exists user"""
        res = self.client.post(TOKEN_URL,
                               {
                                   'email': 'test@recipe.com',
                                   'password': '1234'
                               })
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_missing_fields(self):
        """Test create token with missing field in payload"""
        res = self.client.post(TOKEN_URL,
                               {'email': 'test@recipe.com', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
