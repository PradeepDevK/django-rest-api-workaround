from django.db import models

# Create your models here.
class Tasks(models.Model):
    """Simple Todo Tasks Lists"""
    name = models.CharField(max_length=255)
    priority = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name