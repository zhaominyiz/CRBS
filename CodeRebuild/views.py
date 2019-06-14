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
            # myFile =request.FILES.get("file", None)
            # print(userName,myFile)
            myFile = request.FILES.get("file", None)
            print(userName,myFile)
            lop = request.POST.get('lop')
            if lop == '1':
                for_to_while = 1
            elif lop == '2':
                for_to_while = -1
            else:
                for_to_while = 0
            select = request.POST.get('select')
            if select == '1':
                switch_to_if = 1
            elif select == '2':
                switch_to_if = -1
            else:
                switch_to_if = 0
            multiif = request.POST.get('multiif')
            if multiif == '1':
                multiif_to_if = 1
            elif multiif == '2':
                multiif_to_if = -1
            else:
                multiif_to_if = 0
            language = request.POST.get('lang')
            caption = request.POST.get('caption')
            description = request.POST.get('description')
            algorithm = request.POST.get('algorithm')
            print("cap",caption)
        except:
            msg = 'INPUT_DATAERROR'
        else:
            user_list = models.User.objects.filter(name=userName)
            if len(user_list)==0:
                msg='ACCOUNT_ERROR'
            else:
                coderebuildtask.delay(myFile,userName,multiif_to_if,for_to_while,switch_to_if,language,caption,description,algorithm)
                msg='SUCCESS'
    except:
        msg='SERVE_ERROR'
        # 添加响应头
    response=JsonResponse({
        'msg':msg
    })
    # org = request.headers['Origin']
    # response["Access-Control-Allow-Origin"] = org
    return response

def getqueue(request):
    msg = ''
    list=[]
    try:
        try:
            userName = request.POST.get('userName')
            print("???",userName)
            page = int(request.POST.get('page'))
            pagesize = int(request.POST.get('pageSize'))
        except:
            msg = 'INPUT_DATAERROR'
        else:
            user_list = models.User.objects.filter(name=userName)
            if len(user_list) == 0:
                msg = 'ACCOUNT_ERROR'
            else:
                msg = 'SUCCESS'
                task_list = models.Task.objects.filter(user=user_list[0])
                listlen = len(task_list)
                pagecnt = (listlen+pagesize-1)//pagesize
                for onetask in task_list[(page-1)*pagesize : min(page*pagesize, listlen)]:
                    list.append({
                        'id':onetask.taskid ,
                        'status':onetask.status,
                        'filename':onetask.filename,
                        'time' : onetask.time,
                        'language' : onetask.language,
                        'caption' : onetask.caption,
                        'description' : onetask.description,
                        'algorithm' : onetask.algorithm
                    })
    except:
        msg = 'SERVE_ERROR'


    if (msg != 'SUCCESS'):
        response = JsonResponse({
            'msg': msg
        })
    else:
        response = JsonResponse({
            'msg': msg ,
            'cnt': pagecnt ,
            'list': list
        })
    # 添加响应头
    # org = request.headers['Origin']
    # response["Access-Control-Allow-Origin"] = org
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