from datetime import time
from django.db import models
from django.utils import timezone
from django.conf import settings
# Create your models here.

class Task(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    task_name = models.CharField(max_length=50, null=False)
    task_description = models.TextField(null=True)
    task_category = models.CharField(max_length = 30, default="GENERAL", null=False)
    task_created_date = models.DateTimeField(default=timezone.now, null=False)
    task_alert_time = models.DateTimeField(default=None, null=True)
    task_done = models.BooleanField(default=False, null=False)
    task_archieved = models.BooleanField(default=False, null=False)

    def add_task(self):
        self.task_created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.task_name
