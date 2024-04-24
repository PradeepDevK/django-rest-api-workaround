from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view

from todo_api import models
from todo_api import serializers


@api_view(['GET', 'POST'])
def todo_list(request):
    """Get list of ToDo(s) and Add ToDo"""
    if request.method == 'GET':
        queryset = models.Tasks.objects.all()

        serializer = serializers.ToDoSerializer(queryset, many = True)
        return JsonResponse({ 'data': serializer.data })
    elif request.method == 'POST':
        serializer = serializers.ToDoSerializer(data = JSONParser().parse(request))

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({ 
                'data': serializer.data 
                }, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail(request, pk=None):
    """Update, Fetch and Delete Todo by Id"""
    try:
        queryset = models.Tasks.objects.get(id=pk)
    except models.Tasks.DoesNotExist:
        return JsonResponse({
            'message': "ToDo not found!"
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = serializers.ToDoSerializer(queryset)
        return JsonResponse({
            'data': serializer.data
        })
    elif request.method == 'PUT':
        serializer = serializers.ToDoSerializer(queryset, data = JSONParser().parse(request))

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({ 
                'data': serializer.data 
                }, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        queryset.delete()
        return JsonResponse({
            'message': 'ToDo deleted successfully!'
            }, status=status.HTTP_204_NO_CONTENT)

