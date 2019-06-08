from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    realname = models.CharField(max_length=30)

class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    taskid = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    orgile = models.CharField(max_length=120)
    nowfile = models.CharField(max_length=120)

