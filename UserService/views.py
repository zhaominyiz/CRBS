from django.shortcuts import render
#celery worker -A CRBS -l debug

# Create your views here.
from django.shortcuts import render,HttpResponse
from UserService import tasks

def show(request):
    res = tasks.add.delay(10,4)
    print("start running task")
    print("async task res",res )
    return HttpResponse('结果: %s'%res)