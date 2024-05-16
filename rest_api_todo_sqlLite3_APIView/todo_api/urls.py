from django.urls import path
from rest_framework import permissions


from todo_api import views

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="ToDo API",
        default_version='v1',
        description="Welcome to the world of Django",
        terms_of_service="https://www.example.com/terms",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome Django License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('todo-view/', views.ToDoApiView.as_view(), name='todo_list'),
    path('todo-view/<int:pk>/', views.ToDoApiView.as_view(), name='todo_detail'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]