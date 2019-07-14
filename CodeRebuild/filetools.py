from django.http import HttpResponse
import os
import random as Random
"""
@author 赵珉怿 马靖豪
@desc 此类主要用于文件流的一些操作
@date 2019/7/14
@copyright 南京理工大学 计算机科学与工程学院 剁椒鱼头队

"""
"""
@author 赵珉怿
@desc 此函数用于生产一串随机数 随机数将用于命名用户输入的代码
@date 2019/7/14

@input numlength：需要代码的长度
@output num：随机后的结果

"""
def getRandomName(numlength=11):
    num =''
    # 定义一个参与随机的字符表 可以修改它，扩展可能出现的字符
    chars='1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    length=len(chars)-1
    for j in range(numlength):
        num +=chars[Random.randint(0,length)]
    return num

#完成文件的上传
'''
def upload_file(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理 
        myFile =request.FILES.get("code", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile: 
            return (False,"")
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
'''
"""
@author 赵珉怿
@desc 此函数用于处理上传的代码，将其保存至本地
@date 2019/7/14

@input myFile：上传的文件名 randname：随机产生的文件名
@output num：随机后的结果

"""
def upload_file(myFile , randname):

    randname+='.'+myFile.name.split(".")[1]
    destination = open(os.path.join("tmp", randname), 'wb+')
    for chunk in myFile.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    return randname

"""
@author 赵珉怿
@desc 此函数用于将指定的文件读入，并且保存至数组中
@date 2019/7/14

@input name：上传的文件名 folder：文件所在的目录
@output result：结果的数组

"""
def readCode(name,folder):
    file = open(os.path.join(folder,name),'r',encoding='UTF-8')
    result=[]
    for line in file:
        result.append(line)
        # print(line+"KEKE")
    file.close()
    return result

"""
@author 赵珉怿
@desc 此函数用于采用checkstyle检查代码
@date 2019/7/14

@input name：上传的文件名 folder：文件所在的目录
@output result：结果的数组

"""
def checkstyle(name,floder):
    tool=os.path.join("Utils","checkstyle-8.21-all.jar")
    target=os.path.join(floder,name)
    command='java -jar '+tool+' '+target+' -c /google_checks.xml >tmp/'+name.split('.')[0]+'.txt'
    print("cmd:"+command)
    os.system(command)
    return readCode(name.split('.')[0]+'.txt',"tmp")

"""
@author 赵珉怿
@desc 此函数用于依照输入的str 将指定的文件写入
@date 2019/7/14

@input name：上传的文件名 folder：文件所在的目录 str：需要写入的数组
@output result：结果的数组

"""
def writetxt(name,folder,str):
    # print("???"+os.path.join(folder, name))
    try:
        if os.path.exists(os.path.join(folder, name)):
            os.remove(os.path.join(folder, name))
        file = open(os.path.join(folder, name), 'a', encoding='UTF-8')
        for line in str:
            file.write(line)
        file.close()
    except:
        print("文件写入失败")
        return False
    return True