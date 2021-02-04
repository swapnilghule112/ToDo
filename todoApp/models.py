from datetime import time
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.FileField(upload_to=user_directory_path,default="default_user/default.jpg", null=True)
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Category(models.Model):
    category_name = models.CharField(max_length=20, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    def __str__(self) -> str:
        return self.category_name


class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    task_name = models.CharField(max_length=50, null=False)
    task_description = models.CharField(max_length=150,null=True)
    task_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    task_created_date = models.DateField(default=timezone.now, null=False)
    task_alert_time = models.DateField(default=None, null=True)
    task_done = models.BooleanField(default=False, null=False)
    task_archieved = models.BooleanField(default=False, null=False)

    def add_task(self):
        self.task_created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.task_name
