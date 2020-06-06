from rest_framework import serializers
from recipe import models


class TagSerializer(serializers.ModelSerializer):
    """Serializer for TAG object"""

    class Meta:
        model = models.Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)
