from django.urls import path, include


from api.views import (
    BlogPostListCreateView,
    BlogPostRetrieveUpdateDestroy,
    BlogPostList,
)

urlpatterns = [
    path('blogposts/', BlogPostListCreateView.as_view(), name='blogpost-view-create'),
    path('blogposts/<int:pk>/', BlogPostRetrieveUpdateDestroy.as_view(), name='update'),
    path('blogpost_list/', BlogPostList.as_view(), name='blogpost_list'),
]
