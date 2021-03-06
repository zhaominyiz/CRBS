
# Create your views here.
from django.shortcuts import render,HttpResponse
from UserService import models
import json
from django.http import JsonResponse

def login(request):
    a={}
    msg=""
    try:
        try:
            print(request.POST)
            userName=request.POST.get('userName')
            password=request.POST.get('password')
            print(userName,password)
        except:
            msg='INPUT_DATAERROR'
        else:
            user_list = models.User.objects.filter(name=userName)
            #print(user_list)
            if len(user_list)==0:
                msg='ACCOUNT_ERROR'
            elif user_list[0].password!=password:
                msg='PASSOWRD_ERROR'
            else:
                msg='SUCCESS'
    except:
        msg='SERVE_ERROR'
    # return JsonResponse({
    #     'username':userName,
    #     'msg': msg
    # })

    # return HttpResponse(json.dumps(a, ensure_ascii=Falsresponse =JsonResponse({
    #         'username':userName,
    #         'msg': msg
    #     })
    response = JsonResponse({
        'msg': msg,
        'username':userName
    })
    # 添加响应头
    org=request.headers['Origin']
    response["Access-Control-Allow-Origin"]=org
    return response

def signup(request):
    msg=''
    try:
        try:
            userName = request.POST.get('userName')
            password = request.POST.get('password')
            realName = 'N/A'
        except:
            msg = 'INPUT_DATAERROR'
        else:
            user_list = models.User.objects.filter(name=userName)
            if len(user_list)>0:
                msg='ACCOUNT_ERROR'
            else:
                models.User.objects.create(name=userName, password=password, realname=realName)
                msg='SUCCESS'
    except:
        msg='SERVE_ERROR'
    response = JsonResponse({
        'msg': msg
    })
    # 添加响应头
    org = request.headers['Origin']
    response["Access-Control-Allow-Origin"] = org
    return response
