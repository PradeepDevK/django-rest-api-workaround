"""
URL for tutorial API's
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tutorial import views

# router = DefaultRouter()
# router.register('tutorials', views.TutorialViewSet)

urlpatterns = [
    # ModelViewSet
    # path('', include(router.urls))
    
    # Generic APIView
    # path('tutorials/', views.TutorialListCreateAPIView.as_view(), name='tutorial-list-create'),
    # path('tutorials/<int:pk>/', views.TutorialRetrieveUpdateDestroyAPIView.as_view(), name='tutorial-detail')
    
    # Mixins
    path('tutorials/', views.TutorialListCreateView.as_view(), name='tutorial-list-create'),
    path('tutorials/<int:pk>/', views.TutorialRetrieveUpdateDestroyView.as_view(), name='tuotiral-detail')
]