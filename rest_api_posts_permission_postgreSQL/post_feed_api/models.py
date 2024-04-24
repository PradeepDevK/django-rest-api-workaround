from django.db import models

class Posts(models.Model):
    """Simple User Posts List"""
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=255, blank=False, default='')
    published = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
