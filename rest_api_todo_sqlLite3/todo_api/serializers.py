from rest_framework import serializers
from todo_api import models


class TodoSerializer(serializers.ModelSerializer):
    """Serializes a ToDo Object"""


    class Meta:
        model = models.Tasks
        fields = ('id', 'name', 'priority', 'created_on')
        read_only_fields = ('id', )