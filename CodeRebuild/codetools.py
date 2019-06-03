import os
import CodeRebuild.filetools as filetools
import re
from django.http import HttpResponse
def solve(filename):
    code = filetools.readCode(filename,"tmp")
    code = solveFirst(code,filename)
    # code = solveSecond(code, filename)
    # code = solveThird(code, filename)
    # solveFirst(code,filename)
    return HttpResponse("Success")

#生成空格的函数
def getBlock(cnt):
    str=''
    for i in range(0,cnt):
        str+=' '
    return str

#解决需求1的方法，输入为code[]，输出应为解决掉问题的code[]，作为下一步输出
#此步应当解决代码格式问题
def fixLeftAndEmpty(code):
    for i in range(0,len(code)):
        code[i]=code[i].lstrip()
        flag = False
        print(code[i],len(code[i]))
        j=0
        while j<len(code[i]):

            if code[i][j]=='\"':
                flag =True
                j+=1
                continue
            if code[i][j]=='\"' and flag and code[i][j-1]!='\\':
                flag = False
                j+=1
                continue
            if code[i][j]==' 'and code[i][j+1]==' ' and flag==False:
                strlist = list(code[i])
                del strlist[j+1]
                code[i]="".join(strlist)
                j-=1
            if code[i][j] == ' ' and code[i][j + 1] == ';'and flag==False:
                strlist = list(code[i])
                del strlist[j]
                code[i] = "".join(strlist)
                j -= 1

            j+=1
    return code
#TODO 对此代码进行测试
def solveFirst(code,filename):

    code = fixLeftAndEmpty(code)
    filetools.writetxt(filename,"result",code)

    #先去除一行的多条语句
    for u in range(0,len(code)):
        for v in range(0,len(code[u])):
            if code[u][v]==';' and v>0 and code[u][v-1]!='\\' and code[u][v+1]!='\n':
                strlist = list(code[u])
                strlist.insert(v + 1,'\n')
                code[u] = "".join(strlist)
    for u in range(0,len(code)):
        if 'case' in code[u] or 'default' in code[u]:
            strlist = list(code[u])
            tmp = 0
            for v in range(0,len(code[u])):
                if code[u][v]==':' and code[u][v-1]!='\\':
                    tmp = v
                    break
            strlist.insert(tmp+1,'\n')
            code[u] = "".join(strlist)


    filetools.writetxt("1_"+filename, "result", code)
    code = filetools.readCode("1_"+filename, "result")
    analize = filetools.checkstyle("1_"+filename,"result")

    i = 0
    j = 1
    lazy = -1
    lazy2 = -1
    line_tag = 0

    #再消除需要括号
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
                    strlist.insert(k+1,'{\n')
                    code[i] = "".join(strlist)
                    break
                if "else" in code[i]:
                    cnt = code[i].index('else')
                    strlist = list(code[i])
                    if lazy == linecnt:
                        strlist.insert(k + 4, '{\n')
                    else:
                        strlist.insert(k + 4, '{\n')
                    code[i] = "".join(strlist)
                    break

        # print("修改后CODE=", code[i])
        j+=1

    #消除一下多余空格再重新写入
    filetools.writetxt("2_"+filename, "result", code)
    code = filetools.readCode("2_"+filename,"result")
    result = []
    for i in range(0,len(code)):
        code[i]=code[i].lstrip()
        if code[i]=='\n' or code[i]=='':
            continue
        else:
            result.append(code[i])
    code =result
    filetools.writetxt("2_"+filename, "result", code)
    code = filetools.readCode("2_"+filename, "result")
    analize = filetools.checkstyle("2_"+filename, "result")

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
        j+=1

    filetools.writetxt(filename,"result",code)
    code = filetools.readCode(filename,"result")
    for i in range(0,len(code)):
        if i>0 and code[i][0]=='/':
            code[i] = getBlock(1 * (len(code[i - 1]) - len(code[i - 1].lstrip()))) + code[i]
        elif code[i][0] == 'b' and code[i][1]=='r' and code[i][2] == 'e' and code[i][3]=='a' and code[i][4]=='k':
            code[i] = getBlock(1 * (len(code[i - 1]) - len(code[i - 1].lstrip()))) + code[i]

    filetools.writetxt(filename, "result", code)
    return filetools.readCode(filename,"result")

#解决需求2的方法，输入为code[]，输出应为解决掉问题的code[]，作为下一步输出
#TODO 实现本函数
def solveSecond(code,filename):
    # analize = filetools.checkstyle(filename,"result")
    file1 = open(os.path.join("words.txt"), 'r', encoding='UTF-8')
    # words = ['banana', 'apple', 'number']
    words = []
    line = file1.readline()
    while line:
        line = file1.readline()
        words.append(line[:len(line) - 1])
        # words.append("'"+line+"'")
    # words.append('banana')
    print(words)
    membername = []
    classname = []
    constname = []
    # 注释问题
    keyword = ['abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue',
               'default', 'do', 'double', 'else', 'enum', 'extends', 'final', 'finally', 'float', 'for', 'goto', 'if',
               'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 'private',
               'protected', 'public', 'return', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized',
               'this',
               'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while']
    base = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char']
    for codes in code:
        classflag = False
        constflag = False
        memberflag = False
        tmp = re.split('[ ;]', codes)
        for i in tmp:
            if i.isalnum() == False or len(i) == 0 or (i[0] >= '0' and i[0] <= '9'):
                continue
            if i == 'class':
                classflag = True
                constflag = False
                memberflag = False
            elif i == 'final':
                constflag = True
                classflag = False
                memberflag = False
            elif i == 'static':
                continue
            elif i in base:
                memberflag = True
                classflag = False
                constflag = False
            elif i in keyword:
                continue
            else:
                if classflag:
                    classname.append(i)
                elif constflag:
                    constname.append(i)
                else:
                    membername.append(i)
    result = []

    print("classname")
    print(classname)
    print("const:")
    print(constname)
    print("bianliang:")
    print(membername)

    for codes in code:
        print("codes:"+codes)
        tmp = re.split('[ ;]', codes)
        tmpresult = ''
        # print('tmp')
        # print(tmp)
        cur = 0
        for i in tmp:
            while codes[cur] == ' ':
                tmpresult += ' '
                cur = cur + 1
            cur = cur + len(i)
            if i in keyword:
                tmpresult += i
            elif i in constname:
                tmp1 = i.upper()
                tmpresult += tmp1
            elif (i in classname) or (len(i) > 1 and i[-1] == '{' and i[:-1] in classname) or \
                    (len(i) > 3 and i[-1] == '\n' and i[-2] == '{' and i[:-2] in classname):
                tmp1 = i[:1].upper() + i[1:].lower()
                for j in words:
                    index = tmp1.find(j)
                    if index != -1:
                        pass
                        tmp1 = tmp1.replace(j, j.title())

                tmpresult += tmp1
            elif i in membername:
                tmp1 = i.lower()
                for j in words:
                    index = tmp1.find(j)
                    if index == -1:
                        continue
                    tmp1 = tmp1.replace(j, j.title())
                tmpresult += tmp1
            else:
                tmpresult += i
        result.append(tmpresult)
    for code in result:
        print(code, end='')

    return filetools.writetxt(filename,"result",result)


#解决需求3的方法，输入为code[]，输出应为解决掉问题的code[]，作为下一步输出
#TODO 实现本函数
def solveThird(code,filename):
    analize = filetools.checkstyle(filename,"result")
    return

