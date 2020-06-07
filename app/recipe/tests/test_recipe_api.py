from django.test import TestCase
from django.contrib.auth import get_user_model
from recipe import models


def sample_user(email='test@recipe.com', password='test1234'):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(email, password)


class TestRecipeApi(TestCase):
    """Test the api endpoints"""
    def test_recipe_str(self):
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minute=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)
