from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from recipe import models
from recipe import serializers
TAGS_URL = reverse('recipe:tag-list')


def sample_user(email='test@recipe.com', password='test1234'):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(email, password)


class TagApiTest(TestCase):
    """Test the api endpoints"""

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)


class PublicTagApiTests(TestCase):
    """Test the publiclt available TAG API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to get the tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTests(TestCase):
    """Test the authorized user access TAGs API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@recipe.com',
            password='test1234'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """Test retrieving TAGs"""
        models.Tag.objects.create(user=self.user, name='Vegan')
        models.Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)
        tags = models.Tag.objects.all().order_by('-name')
        serializer = serializers.TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@recipe.com',
            'test1234'
        )

        models.Tag.objects.create(user=user2, name='Fruity')
        tag = models.Tag.objects.create(user=self.user, name='Comfort food')

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
