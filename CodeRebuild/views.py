from django.shortcuts import render
from django.http import HttpResponse
import CodeRebuild.filetools as filetools
import CodeRebuild.codetools as codetools
# Create your views here.

def helloWorld(request):
    return HttpResponse("hello world!")

def testPost(request):
    str=request.POST.get("msg")
    return HttpResponse("Recive msg"+str)

def receiveTask(request):
    (flag,name)=filetools.upload_file(request)
    if flag==False:
        return HttpResponse("Error")
    else:
        return codetools.solve(name)