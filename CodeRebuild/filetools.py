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

#完成文件的上传
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

#输入文件名,文件夹，输出成list的代码
def readCode(name,folder):
    file = open(os.path.join(folder,name),'r',encoding='UTF-8')
    result=[]
    for line in file:
        result.append(line)
        # print(line+"KEKE")
    file.close()
    return result

#输入文件名，调用CheckStyle对文件名分析，并且返回list
def checkstyle(name,floder):
    tool=os.path.join("Utils","checkstyle-8.21-all.jar")
    target=os.path.join(floder,name)
    command='java -jar '+tool+' '+target+' -c /google_checks.xml >tmp/'+name.split('.')[0]+'.txt'
    print("cmd:"+command)
    os.system(command)
    return readCode(name.split('.')[0]+'.txt',"tmp")

#输入文件名，文件夹，文本列表，写入
def writetxt(name,folder,str):
    # print("???"+os.path.join(folder, name))
    try:
        if os.path.exists(os.path.join(folder, name)):
            os.remove(os.path.join(folder, name))
        file = open(os.path.join(folder, name), 'a', encoding='UTF-8')
        for line in str:
            # print("l="+line)
            file.write(line)
        file.close()
    except:
        print("文件写入失败")
        return False
    return True