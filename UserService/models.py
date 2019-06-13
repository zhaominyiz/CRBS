from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    realname = models.CharField(max_length=30)

class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    taskid = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    orgfile = models.CharField(max_length=120)
    nowfile = models.CharField(max_length=120)
    caption = models.CharField(max_length=120)
    description = models.CharField(max_length=1023)
    language = models.CharField(max_length=30)
    time = models.DateTimeField(default = timezone.now)
    filename = models.CharField(max_length=120)
    algorithm = models.CharField(max_length=30)
