from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from recipe.models import Tag, Ingredient, Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer
RECIPE_URL = reverse('recipe:recipe-list')


def sample_user(email='test@recipe.com', password='test1234'):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(email, password)


def sample_tag(user, name='Main course'):
    """Create and return a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredient(user, name='Cinnamon'):
    """Create and return a sample ingredient"""
    return Ingredient.objects.create(user=user, name=name)


def recipe_details_url(recipe_id):
    """generate and return recipe url"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_recipe(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        'title': 'Test recipe',
        'price': 5.00,
        'time_minutes': 5,
    }
    defaults.update(params)
    return Recipe.objects.create(
        user=user,
        **defaults
    )


class TestRecipeApi(TestCase):
    """Test the api endpoints"""
    def test_recipe_str(self):
        recipe = Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)


class PublicRecipeApiTest(TestCase):
    """Test unauthenticated api test case"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication is required"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Test authenticated recipe api access"""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@recipe.com', 'test123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            'other@recipe.com', 'test123'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_detail_recipe(self):
        """Test detail of a recipe api"""
        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = recipe_details_url(recipe.id)

        res = self.client.get(url)

        serializer = RecipeDetailSerializer(res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
