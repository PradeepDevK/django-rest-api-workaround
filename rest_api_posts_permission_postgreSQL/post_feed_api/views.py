from rest_framework import viewsets


from post_feed_api import models
from post_feed_api import serializers

"""
ModelViewSet With queryset and serialize_class
"""
class PostViewSet(viewsets.ModelViewSet):
    """Posts API ViewSet"""
    queryset = models.Posts.objects.all()
    serializer_class = serializers.PostSerializer

    