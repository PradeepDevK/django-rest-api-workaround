from django.urls import path, include
# from watchlist_app.api.views import (
#     movie_list,
#     movie_details
# )

from watchlist_app.api.views import (
    WatchListAPIView,
    WatchDetailsAPIView,
    StreamPlatformListAPIView,
    StreamPlatformDetailAPIView,
)

urlpatterns = [
    # path('list/', movie_list, name='movie_list'),
    # path('<int:pk>/', movie_details, name='movie_details')
    path('list/', WatchListAPIView.as_view(), name='movie_list'),
    path('<int:pk>/', WatchDetailsAPIView.as_view(), name='movie_details'),
    path('stream/', StreamPlatformListAPIView.as_view(), name='platform_list'),
    path('stream/<int:pk>/', StreamPlatformDetailAPIView.as_view(), name='streamplatform-detail'),
]
