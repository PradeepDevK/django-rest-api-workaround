from django.db import models


class Tasks(models.Model):
    """Simple ToDo Tasks List"""
    name = models.CharField(max_length=255)
    priority = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
