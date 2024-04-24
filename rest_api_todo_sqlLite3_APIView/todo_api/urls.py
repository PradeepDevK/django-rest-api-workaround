from django.urls import path

from todo_api import views

urlpatterns = [
    path('todo-view/', views.ToDoApiView.as_view(), name='todo-list'),
    path('todo-view/<int:pk>/', views.ToDoApiView.as_view(), name='todo-detail')
]