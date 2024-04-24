from django.urls import path, include
from rest_framework.routers import DefaultRouter

from todo_api import views

router = DefaultRouter()
# router.register('todo', views.TodoViewSet)
"""
When you're using a ViewSet and without specifying the 'queryset' and 'serializer_class' 
then you need to  provide a basename argument in the router.register
"""
router.register('pradeep', views.TodoViewSet, basename = 'todo-viewset')

urlpatterns = [
    path('', include(router.urls))
]