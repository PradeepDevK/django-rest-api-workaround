from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


from todo_api import models
from todo_api import serializers


class ToDoApiView(APIView):
    """ToDo API View"""
    serializer_class = serializers.ToDoSerializer

    @swagger_auto_schema(operation_description="Get ToDo List and as well as by pk(primary key)")
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
    
    @swagger_auto_schema(
        operation_description="Add New ToDo",
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'priority'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'priority': openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    ))
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
        
    @swagger_auto_schema(
        operation_description="Update ToDo by pk",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Primary key of the ToDo", type=openapi.TYPE_INTEGER)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'priority'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'priority': openapi.Schema(type=openapi.TYPE_INTEGER),
        })
    )
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
        
    @swagger_auto_schema(
        operation_description="Update part of a ToDo by pk",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Primary key of the ToDo", type=openapi.TYPE_INTEGER)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'priority'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'priority': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        )
    )
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
        
    @swagger_auto_schema(
        operation_description="Delete ToDo by pk",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="Primary key of the ToDo", type=openapi.TYPE_INTEGER)
        ]
    )
    def delete(self, request, pk):
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
