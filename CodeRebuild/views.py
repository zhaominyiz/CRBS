from django.shortcuts import render
from django.http import HttpResponse
from UserService import models
import json
from django.http import JsonResponse
import os
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

def getqueue(request):
    msg = ''
    list=[]
    try:
        try:
            userName = request.POST.get('userName')
        except:
            msg = 'INPUT_DATAERROR'
        else:
            user_list = models.User.objects.filter(name=userName)
            if len(user_list) == 0:
                msg = 'ACCOUNT_ERROR'
            else:
                msg = 'SUCCESS'
                task_list = models.Task.objects.filter(user=user_list[0])
                for onetask in task_list:
                    list.append({'id':onetask.taskid , 'status':onetask.status})
    except:
        msg = 'SERVE_ERROR'
    if (msg != 'SUCCESS'):
        response = JsonResponse({
            'msg': msg
        })
    else:
        response = JsonResponse({
            'msg': msg ,
            'list': list
        })
    # 添加响应头
    org = request.headers['Origin']
    response["Access-Control-Allow-Origin"] = org
    return response

def getdetail(request):
    msg = ''
    try:
        try:
            userName = request.POST.get('userName')
            taskid = request.POST.get('id')
        except:
            msg = 'INPUT_DATAERROR'
        else:
            user_list = models.User.objects.filter(name=userName)
            if len(user_list) == 0:
                msg = 'ACCOUNT_ERROR'
            else:
                task_list = models.Task.objects.filter(user=user_list[0] , taskid=taskid)
                if len(task_list) == 0 or task_list[0].status != 'FINISHED':
                    msg = 'TASKID_ERROR'
                else:
                    orgFile = os.path.join("tmp", task_list[0].orgfile)
                    file = open(orgFile, 'r', encoding='UTF-8')
                    orgText = file.read()
                    file.close()
                    orgFile = os.path.dirname(os.path.abspath(orgFile))
                    nowFile = os.path.join("result", task_list[0].nowfile)
                    file = open(nowFile, 'r', encoding='UTF-8')
                    nowText = file.read()
                    file.close()
                    nowFile = os.path.dirname(os.path.abspath(nowFile))
                    msg='SUCCESS'
    except:
        msg = 'SERVE_ERROR'
    if(msg != 'SUCCESS'):
        response = JsonResponse({
            'msg':msg
        })
    else:
        response = JsonResponse({
            'msg': msg,
            'orgFile':orgFile,
            'orgText':orgText,
            'nowFIle':nowFile,
            'nowText':nowText
        })
    # 添加响应头
    org = request.headers['Origin']
    response["Access-Control-Allow-Origin"] = org
    return response

def testadd1(request):
    from CodeRebuild.tasks import add
    result =add.delay(4,5)
    return HttpResponse("haha")