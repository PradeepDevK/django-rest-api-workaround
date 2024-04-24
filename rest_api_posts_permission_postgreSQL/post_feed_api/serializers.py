from rest_framework import serializers
from post_feed_api import models


class PostSerializer(serializers.ModelSerializer):
    """Serializes a Post Object"""


    class Meta:
        model = models.Posts
        fields = ('id', 'title', 'description', 'published', 'created_on')
        read_only_fields = ('id', 'created_on')