from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.views import APIView

from watchlist_app.models import (
    WatchList,
    StreamPlatform
)
from watchlist_app.api.serializers import (
    WatchListSerializer,
    StreamPlatformSerializer
)

class WatchListAPIView(APIView):
    
    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class WatchDetailsAPIView(APIView):
    
    def get(self, request, pk=None):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk=None):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk=None):
        try:
            movie = WatchList.objects.get(pk=pk)
            movie.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except WatchList.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
class StreamPlatformListAPIView(APIView):
    
    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class StreamPlatformDetailAPIView(APIView):
    
    def get(self, request, pk=None):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self, request, pk=None):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk=None):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            platform.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except StreamPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
        
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk=None):
    
#     if request.method == 'GET':       
#         try:
#             movie = Movie.objects.get(pk=pk)            
#         except Movie.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND) 
        
#         serializer = MovieSerializer(movie)    
#         return Response(serializer.data)       
    
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        
    