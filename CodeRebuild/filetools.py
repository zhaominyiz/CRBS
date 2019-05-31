from django.http import HttpResponse
import os
import random as Random
def getRandomName(numlength=11):
    num =''
    chars='1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    length=len(chars)-1
    for j in range(numlength):
        num +=chars[Random.randint(0,length)]
    return num

def upload_file(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理 
        myFile =request.FILES.get("code", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile: 
            return (False,"")
        j = 10
        randname=getRandomName()
        # print(myFile.name+","+randname)
        filetype=myFile.name.split(".")
        # print(filetype)
        randname+='.'+filetype[1]
        destination = open(os.path.join("tmp",randname),'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件 
            destination.write(chunk) 
        destination.close() 
        return (True,randname)

def readCode(name):
    file = open(os.path.join("tmp",name),'r',encoding='UTF-8')
    result=[]
    for line in file:
        result.append(line)
        # print(line+"KEKE")
    file.close()
    return result

def checkstyle(name):
    tool=os.path.join("Utils","checkstyle-8.21-all.jar")
    target=os.path.join("tmp",name)
    command='java -jar '+tool+' '+target+' -c /google_checks.xml >tmp/'+name.split('.')[0]+'.txt'
    # print(command)
    os.system(command)
    return readCode(name.split('.')[0]+'.txt')