from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from todo_api import models
from todo_api import serializers


class ToDoApiView(APIView):
    """ToDo API View"""
    serializer_class = serializers.ToDoSerializer

    def get(self, request, pk=None):
        """Returns list of ToDo(s) | by ID"""
        if pk is not None:
            try:
                queryset = models.Tasks.objects.get(id=pk)
                serializer = self.serializer_class(queryset)
                return Response({
                    'message': 'Success',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            except models.Tasks.DoesNotExist:
                return Response({'message': 'Failed'}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = models.Tasks.objects.all()
            serializer = self.serializer_class(queryset, many=True)
            return Response({
                'message': 'Success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)            
    
    def post(self, request):
        """Create a new ToDo"""
        serializer = self.serializer_class(data=request.data)

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
        
    def put(self, request, pk=None):
        """Handle Updating an Object"""
        if pk is not None:
            try:
                instance = models.Tasks.objects.get(id=pk)
                serializer = self.serializer_class(instance, data = request.data)
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
        else:
            return Response({
                'error': 'Please provide a valid ToDo ID.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pk=None):
        """Handle updating part of an object"""
        if pk is not None:
            try:
                instance = models.Tasks.objects.get(id=pk)
                serializer = self.serializer_class(instance, data = request.data, partial = True)
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
        else:
            return Response({
                'error': 'Please provide a valid ToDo ID.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk=None):
        """Delete an object"""
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
