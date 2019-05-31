import os
import CodeRebuild.filetools as filetools
from django.http import HttpResponse
def solve(filename):
    code=filetools.readCode(filename)
    # str="".join(code)+"\n"+"".join(analize)
    # print(str)
    code = solveFirst(code,filename)
    code = solveSecond(code, filename)
    code = solveThird(code, filename)
    solveFirst(code,filename)
    return HttpResponse("Success")

#解决需求1的方法，输入为code[]，输出应为解决掉问题的code[]，作为下一步输出
#TODO 实现本函数
def solveFirst(code,filename):
    analize = filetools.checkstyle(filename)
    return

#解决需求2的方法，输入为code[]，输出应为解决掉问题的code[]，作为下一步输出
#TODO 实现本函数
def solveSecond(code,filename):
    analize = filetools.checkstyle(filename)
    return

#解决需求3的方法，输入为code[]，输出应为解决掉问题的code[]，作为下一步输出
#TODO 实现本函数
def solveThird(code,filename):
    analize = filetools.checkstyle(filename)
    return

