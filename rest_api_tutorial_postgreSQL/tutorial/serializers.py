"""
Serializer for Tutorial API's
"""

from rest_framework import serializers
from .models import Tutorial

class TutorialSerializer(serializers.ModelSerializer):
    """
    Serializer for Tutorial
    """

    class Meta:
        model = Tutorial
        fields = '__all__'