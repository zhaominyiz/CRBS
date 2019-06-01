import os
import CodeRebuild.filetools as filetools
import re
from django.http import HttpResponse
def solve(filename):
    code=filetools.readCode(filename,"tmp")
    # str="".join(code)+"\n"+"".join(analize)
    # print(str)
    code = solveFirst(code,filename)
    # code = solveSecond(code, filename)
    # code = solveThird(code, filename)
    # solveFirst(code,filename)
    return HttpResponse("Success")


def getBlock(cnt):
    str=''
    for i in range(0,cnt):
        str+=' '
    return str

#解决需求1的方法，输入为code[]，输出应为解决掉问题的code[]，作为下一步输出
#此步应当解决代码格式问题
#TODO 对此代码进行测试
def solveFirst(code,filename):
    for i in range(0,len(code)):
        code[i]=code[i].lstrip()
        # print(code[i])
    filetools.writetxt(filename,"result",code)
    analize = filetools.checkstyle(filename,"result")
    result = []
    i=0
    j=1
    lazy=-1
    lazy2=-1
    line_tag = 0
    while True:
        #若完了
        if i>=len(code) and j>=len(analize)-1:
            break
        #若报告扫到了最后
        if j>=len(analize)-1:
            # result.append(code[i])
            i+=1
            continue
        #获取行号 我们现在在分析第i+1行
        linecnt = int(analize[j].split(':')[2])
        # print("检查规则" + analize[j])
        linecnt = int(analize[j].split(':')[2])
        # print("行号=", linecnt, "CODE=",code[i])
        if i<linecnt-1:
            # result.append(code[i])
            i+=1
            continue
        # if lazy == linecnt:
        #     code[i]='}\n'+code[i]
        #需要空行，默认为下2行
        if 'NeedBraces' in analize[j]:
            flag = True
            lazy=linecnt
            for k in range(0,len(code[i])):
                if code[i][k]==';' and k!=0 and code[i][k-1]!='\\':
                    flag = False
                    break
            if flag:
                lazy=linecnt+1
            # print("LAZY=",lazy,"CODE=",code[lazy-1])
            code[lazy-1]=code[lazy-1]+'}\n'
            cnt_l = 0
            flag = False
            for k in range(0, len(code[i])):
                # print(k,code[i][k],cnt_l,flag)
                if code[i][k] == '(':
                    flag = True
                    cnt_l += 1
                elif code[i][k] == ')':
                    cnt_l -= 1
                if flag and cnt_l == 0:
                    strlist = list(code[i])
                    strlist.insert(k+1,'{')
                    code[i] = "".join(strlist)
                    break
                if "else" in code[i]:
                    cnt = code[i].index('else')
                    strlist = list(code[i])
                    if lazy == linecnt:
                        strlist.insert(k + 4, '{\n')
                    else:
                        strlist.insert(k + 4, '{')
                    code[i] = "".join(strlist)
                    break

        if 'OneStatementPerLine' in analize[j] and line_tag != linecnt:
            line_tag = linecnt
            lineadd = 1
            flag = True
            while flag:
                flag =  False
                strlist = list(code[i])
                for k in range(0,len(code[i])):
                    if code[i][k]==';'and k-1>=0 and code[i][k-1]!='\\' and k+1<len(code[i]) and code[i][k+1]!='\n':
                        strlist.insert(k+1,'\n')
                        code[i]="".join(strlist)
                        flag = True
                        break
        # print("修改后CODE=", code[i])
        j+=1

    #消除一下多余空格再重新写入
    filetools.writetxt(filename, "result", code)
    code = filetools.readCode(filename,"result")
    for i in range(0,len(code)):
        code[i]=code[i].lstrip()
    filetools.writetxt(filename, "result", code)
    code = filetools.readCode(filename, "result")
    analize = filetools.checkstyle(filename, "result")

    for lines in code:
        print("ll",lines)
    i = 0
    j = 1
    len_tag = -1
    exadd = 0
    record_w = -1
    while True:
        if i>=len(code) and j>=len(analize)-1:
            break
        if j>=len(analize)-1:
            i+=1
            continue

        print("检查规则"+analize[j])
        linecnt=int(analize[j].split(':')[2])
        print("行号=",linecnt,"CODE=",code[i])
        if i<linecnt-1:
            # result.append(code[i])
            i+=1
            continue
        if 'Indentation' in analize[j]:
            regex = r'.*应为(.*)个.*'
            matches = re.findall(regex, analize[j])
            print(matches)
            tapcnt=int(matches[0])
            tapcnt*=2
            str = getBlock(tapcnt)
            # print("此行应当缩进",tapcnt)
            code[i]=str+code[i]

        if 'WhitespaceAround' in analize[j]:
            regex = r".*\'(.*)\'.*"
            matches = re.findall(regex, analize[j])
            # print('matches',matches)
            token=matches[0]
            wordcnt = int(analize[j].split(':')[3])
            tokenlen = len(token)

            strlist = list(code[i])
            lnull = len(code[i])-len(code[i].lstrip())
            print("LENTAG=",line_tag,"WORDCNT=",wordcnt,"EXADD=",exadd)
            if len_tag != linecnt:
                exadd = 0
            len_tag = linecnt
            if 'followed' in analize[j]:
                if record_w == wordcnt:
                    strlist.insert(wordcnt + lnull +tokenlen +exadd -1,' ')
                else:
                    strlist.insert(wordcnt + lnull +tokenlen +exadd -1, ' ')
            else:
                if record_w == wordcnt:
                    strlist.insert(wordcnt + lnull + exadd - 2, ' ')
                else:
                    strlist.insert(wordcnt + lnull +exadd - 1, ' ')
            exadd += 1
            record_w = wordcnt
            code[i] = "".join(strlist)

        print("修改后CODE=",code[i])
        j+=1

    filetools.writetxt(filename,"result",code)


#解决需求2的方法，输入为code[]，输出应为解决掉问题的code[]，作为下一步输出
#TODO 实现本函数
def solveSecond(code,filename):
    analize = filetools.checkstyle(filename,"result")
    return

#解决需求3的方法，输入为code[]，输出应为解决掉问题的code[]，作为下一步输出
#TODO 实现本函数
def solveThird(code,filename):
    analize = filetools.checkstyle(filename,"result")
    return

