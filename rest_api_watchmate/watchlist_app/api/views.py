from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets

from django.shortcuts import get_object_or_404

from rest_framework.throttling import (
    UserRateThrottle,
    AnonRateThrottle,
    ScopedRateThrottle,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from watchlist_app.api.throttling import (
    ReviewCreateThrottle,
    ReviewListThrottle
)
 

from watchlist_app.models import (
    WatchList,
    StreamPlatform,
    Review
)
from watchlist_app.api.serializers import (
    WatchListSerializer,
    StreamPlatformSerializer,
    ReviewSerializer
)

from watchlist_app.api.permissions import (
    IsAdminOrReadOnlyPermission,
    IsReviewUserOrReadOnlyPermission,
)

from watchlist_app.api.pagination import (
    WatchListPagination,
    WatchListOffsetPagination
)


class UserReview(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    
    def get_queryset(self):
        # url params
        # username = self.kwargs['username']
        # return Review.objects.filter(review_user__username=username)
        
        #querystring
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")
        
        if watchlist.number_rating == 0:
            watchlist.average_rating = serializer.validated_data['rating']
        else:
            watchlist.average_rating = (watchlist.average_rating  + serializer.validated_data['rating']) / 2
            
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        
        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_classes = [ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnlyPermission]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review_detail'


# class ReviewDetail(mixins.RetrieveModelMixin,
#                    generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin,
#                 mixins.CreateModelMixin,
#                 generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
       

class StreamPlatformViewSet(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer        
    permission_classes = [IsAdminOrReadOnlyPermission]

 
# class StreamPlatformViewSet(viewsets.ViewSet):
    
    def list(self, request):
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        watchlist = get_object_or_404(queryset, pk=pk)
        serializer = StreamPlatformSerializer(watchlist)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk=None):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
            platform.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except StreamPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
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
   
        
class StreamPlatformListAPIView(APIView):
    permission_classes = [IsAdminOrReadOnlyPermission]
    
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
    permission_classes = [IsAdminOrReadOnlyPermission]
    
    def get(self, request, pk=None):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(platform, )
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


class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListOffsetPagination
    # filter_backends = [DjangoFilterBackend]
    # filter_backends = [filters.SearchFilter]
    filter_backends = [filters.OrderingFilter]
    # filterset_fields = ['title', 'platform__name']
    # search_fields = ['title', 'platform__name']
    ordering_fields = ['average_rating']
        
        
class WatchListAPIView(APIView):
    permission_classes = [IsAdminOrReadOnlyPermission]
    
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
    permission_classes = [IsAdminOrReadOnlyPermission]
    
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
        
    