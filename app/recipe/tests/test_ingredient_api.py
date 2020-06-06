from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from recipe import models
from recipe import serializers
INGREDIENT_URL = reverse('recipe:ingredient-list')


def sample_user(email='test@recipe.com', password='test1234'):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(email, password)


class IngredientApiTest(TestCase):
    """Test the api endpoints"""

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)


class PublicIngredientApiTests(TestCase):
    """Test the publicly available INGREDIENT API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to get the ingredients"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateINgredientApiTests(TestCase):
    """Test the authorized user access INGREDIENTs API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@recipe.com',
            password='test1234'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving INGREDIENTs"""
        models.Ingredient.objects.create(user=self.user, name='Kale')
        models.Ingredient.objects.create(user=self.user, name='Salt')

        res = self.client.get(INGREDIENT_URL)
        tags = models.Ingredient.objects.all().order_by('-name')
        serializer = serializers.IngredientSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@recipe.com',
            'test1234'
        )

        models.Ingredient.objects.create(user=user2, name='Vinegar')
        ingredient = models.Ingredient.objects.create(
            user=self.user, name='Turmeric')

        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_successful(self):
        """Test creating a new ingredient"""
        payload = {'name': 'Test ingredient'}
        self.client.post(INGREDIENT_URL, payload)

        exists = models.Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test creating ingredient failed with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
