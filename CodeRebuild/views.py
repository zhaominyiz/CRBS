from django.shortcuts import render
from django.http import HttpResponse
from UserService import models
import json
# Create your views here.

def helloWorld(request):
    return HttpResponse("hello world!")

def testPost(request):
    str=request.POST.get("msg")
    return HttpResponse("Recive msg"+str)

def receiveTask(request):
    from CodeRebuild.tasks import coderebuildtask
    msg=''
    try:
        try:
            userName = request.POST.get('userName')
            myFile =request.FILES.get("code", None)
        except:
            msg = 'INPUT_DATAERROR'
        else:
            user_list = models.User.objects.filter(name=userName)
            if len(user_list)==0:
                msg='ACCOUNT_ERROR'
            else:
                coderebuildtask.delay(myFile,userName)
                msg='SUCCESS'
    except:
        msg='SERVE_ERROR'
    return HttpResponse(json.dumps(msg, ensure_ascii=False), content_type="application/json,charset=utf-8")

def testadd1(request):
    from CodeRebuild.tasks import add
    result =add.delay(4,5)
    return HttpResponse("haha")