from rest_framework import serializers
from todo_api import models

class ToDoSerializer(serializers.ModelSerializer):
    """Serializer ToDo Object"""

    name = serializers.CharField(max_length=255)
    priority = serializers.IntegerField()

    class Meta:
        model = models.Tasks
        fields = ('id', 'name', 'priority', 'created_on')
        read_only_fields = ('id', 'created_on')

    def create(self, validated_data):
        return models.Tasks.objects.create(**validated_data)
    
    def update(self, instance, validate_data):
        """Handle updating ToDo Object"""
        instance.name = validate_data.get('name', instance.name)
        instance.priority = validate_data.get('priority', instance.priority)

        instance.save()
        return instance


