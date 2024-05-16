from django.db import models


class Tutorial(models.Model):
    """Model for tutorial"""
    title = models.CharField(max_length=255, blank=False, default='')
    description = models.CharField(max_length=255, blank=False, default='')
    published = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title