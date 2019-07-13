from celery import task
from django.http import HttpResponse
import  time
from CodeRebuild import filetools
from CodeRebuild import codetools
from UserService import models

# celery worker -A CRBS -l debug
# celery flower --broker=amqp://myuser:mypassword@localhost:5672/vhost

@task
def add(x,y):
    time.sleep(10)
    print(x+y)
    return

@task
def coderebuildtask(myFile, userName, multiif_to_if, for_to_while, switch_to_if,language,caption,description,algorithm):
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
    p1 = models.Task(user=user , taskid=randname, orgfile=filename, status='RUNNING', nowfile='', filename=myFile.name, language=language, caption=caption, description=description,algorithm=algorithm)
    p1.save()
    try:
        filename = codetools.solve(filename,multiif_to_if,for_to_while,switch_to_if)
        p1.nowfile = filename
        p1.status = "FINISHED"
        p1.save()
    except:
        p1.status = "FAILED"
        p1.save()
    return