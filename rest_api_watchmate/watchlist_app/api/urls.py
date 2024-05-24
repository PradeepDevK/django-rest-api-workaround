from django.urls import path, include
# from watchlist_app.api.views import (
#     movie_list,
#     movie_details
# )
from rest_framework.routers import DefaultRouter


from watchlist_app.api.views import (
    WatchListAPIView,
    WatchDetailsAPIView,
    StreamPlatformListAPIView,
    StreamPlatformDetailAPIView,
    ReviewList,
    ReviewDetail,
    ReviewCreate,
    StreamPlatformViewSet,
    UserReview,
    WatchListGV
)

router = DefaultRouter()
router.register('stream', StreamPlatformViewSet, basename='streamplatform')

urlpatterns = [
    # path('list/', movie_list, name='movie_list'),
    # path('<int:pk>/', movie_details, name='movie_details')
    path('list/', WatchListAPIView.as_view(), name='movie_list'),
    path('<int:pk>/', WatchDetailsAPIView.as_view(), name='movie_details'),
    path('list2/', WatchListGV.as_view(), name='watch_list'),
    path('', include(router.urls)),
    # path('stream/', StreamPlatformListAPIView.as_view(), name='platform_list'),
    # path('stream/<int:pk>/', StreamPlatformDetailAPIView.as_view(), name='streamplatform-detail'),
    # path('review/', ReviewList.as_view(), name='review_list'),
    # path('review/<int:pk>/', ReviewDetail.as_view(), name='review_detail'),
    path('<int:pk>/review_create/', ReviewCreate.as_view(), name='review_create'),
    path('<int:pk>/review/', ReviewList.as_view(), name='review_list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review_detail'),
    # path('reviews/<str:username>/', UserReview.as_view(), name='user_review_detail'),
    path('reviews/', UserReview.as_view(), name='user_review_detail'),
]
