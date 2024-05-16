"""
Views for the tutorial API's
"""

from rest_framework import (
    viewsets,
    mixins,
    generics
)

from tutorial import models
from tutorial import serializers


"""
Example of ModelViewSet
"""
# class TutorialViewSet(viewsets.ModelViewSet):
#     """
#     Viewsets of Tutorial
#     """
#     queryset = models.Tutorial.objects.all()
#     serializer_class = serializers.TutorialSerializer


"""
Example of Generic APIView
"""
# class TutorialListCreateAPIView(generics.ListCreateAPIView):
#     queryset = models.Tutorial.objects.all()
#     serializer_class = serializers.TutorialSerializer

# class TutorialRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Tutorial.objects.all()
#     serializer_class = serializers.TutorialSerializer


"""
Example of mixins
"""
class TutorialListCreateView(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            generics.GenericAPIView):
    queryset = models.Tutorial.objects.all()
    serializer_class = serializers.TutorialSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class TutorialRetrieveUpdateDestroyView(mixins.RetrieveModelMixin,
                                        mixins.UpdateModelMixin,
                                        mixins.DestroyModelMixin,
                                        generics.GenericAPIView):
    queryset = models.Tutorial.objects.all()
    serializer_class = serializers.TutorialSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)