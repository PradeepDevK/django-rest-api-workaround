from rest_framework import viewsets
from rest_framework.mixins import (ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin)
from rest_framework.response import Response
from rest_framework import status

from todo_api import models
from todo_api import serializers


"""
In the below example, ModelViewSet class that automatically provides the CRUD funcitonality
for the "Tasks" model. We just need to specify 'queryset' and 'serializer_class'
# """
# class TodoViewSet(viewsets.ModelViewSet):
#     """ToDo API ViewSet (ModelViewSet)"""
#     queryset = models.Tasks.objects.all()
#     serializer_class = serializers.TodoSerializer



"""
In the below example, generally ModelViewSet is shortcut of combining the common patterns of these mixins,
which provide the CRUD functionality. If you do not want the 'PATCH' API then by removing 'UpdateModelMixin'
from the list of mixins with disable the 'PATCH' and only full updates using 'PUT' request would be allowed.
"""
# class TodoViewSet(ListModelMixin, 
#                   CreateModelMixin,
#                   RetrieveModelMixin,
#                   UpdateModelMixin,
#                   DestroyModelMixin,
#                   viewsets.GenericViewSet
#                   ):
#     """ToDo API ViewSet (ModelViewSet) with mixins"""
#     queryset = models.Tasks.objects.all()
#     serializer_class = serializers.TodoSerializer


"""
If you want to use 'viewsets' without specifying 'queryset' and 'serializer_class' attributes directly, and
instead define the CRUD functions explicitly you can subclass the viewsets.ViewSet and overrride it's methods
accordingly like below
(list, create, update, retrieve, partial_update, destroy)
"""
class TodoViewSet(viewsets.ViewSet):
    """ToDo API with ViewSet"""

    def list(self, request):
        """Return list of ToDo(s)"""
        queryset = models.Tasks.objects.all()
        serializer = serializers.TodoSerializer(queryset, many = True)
        return Response({
            'message': 'Success',
            'data': serializer.data
        })
    
    def create(self, request):
        """Create a new ToDo"""
        serializer = serializers.TodoSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Success',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Failed',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        try:
            instance = models.Tasks.objects.get(id=pk)
            serializer = serializers.TodoSerializer(instance)
            return Response({
                'message': 'Success',
                'data': serializer.data
            })
        except models.Tasks.DoesNotExist:
            return Response({
                'message': 'Failed'
            }, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
        """Handle updating an object"""
        try:
            instance = models.Tasks.objects.get(id=pk)
            serializer = serializers.TodoSerializer(instance, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Success',
                    'data': serializer.data
                })
            else:
                return Response({
                    'message': 'Failed',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except models.Tasks.DoesNotExist:
            return Response({
                'message': 'Failed'
            }, status=status.HTTP_404_NOT_FOUND)
        
    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        try:
            instance = models.Tasks.objects.get(id=pk)
            serializer = serializers.TodoSerializer(instance, data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Success',
                    'data': serializer.data
                })
            else:
                return Response({
                    'message': 'Failed',
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except models.Tasks.DoesNotExist:
            return Response({
                'message': 'Failed'
            }, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        """Handle removing an object"""
        try:
            instance = models.Tasks.objects.get(id=pk)
            instance.delete()
            return Response({
                'message': 'Success'
            }, status=status.HTTP_204_NO_CONTENT)
        except models.Tasks.DoesNotExist:
            return Response({
                'message': 'Failed'
            }, status=status.HTTP_404_NOT_FOUND)

