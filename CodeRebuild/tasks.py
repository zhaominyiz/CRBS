from celery import task
from django.http import HttpResponse
import  time
from CodeRebuild import filetools
from CodeRebuild import codetools
from UserService import models

#celery worker -A CRBS -l debug
#celery flower --broker=amqp://myuser:mypassword@localhost:5672/vhost

@task
def add(x,y):
    time.sleep(10)
    print(x+y)
    return

@task
def coderebuildtask(myFile, userName):
    print("hehe")
    randname=""
    while True:
        randname = filetools.getRandomName()
        tmplist = models.Task.objects.filter(taskid=randname)
        if len(tmplist)==0:
            break
    filename = filetools.upload_file(myFile , randname)
    if filename=='':
        return
    user = models.User.objects.get(name=userName)
    p1 = models.Task(user=user , taskid=randname, orgfile=filename, status='RUNNING', nowfile='')
    p1.save()
    filename = codetools.solve(filename)
    p1.nowfile = filename
    p1.status = "FINISHED"
    p1.save()
    return