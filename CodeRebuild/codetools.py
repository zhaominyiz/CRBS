import os
import CodeRebuild.filetools as filetools
import re
from django.http import HttpResponse
def solve(filename,multiif_to_if,for_to_while,switch_to_if):
    code = filetools.readCode(filename,"tmp")

    code = solveFirst(code,filename)
    for codes in  code:
        print (codes)
    print("现在进入Step2")
    code = solveSecond(code, filename)

    for codes in  code:
        print (codes)

    print("现在进入Step3")
    code = solveThird(code, filename,multiif_to_if,for_to_while,switch_to_if)
    # solveFirst(code,filename)
    return filename

#生成空格的函数
def getBlock(cnt):
    str=''
    for i in range(0,cnt):
        str+=' '
    return str

#解决需求1的方法，输入为code[]，输出应为解决掉问题的code[]，作为下一步输出
#此步应当解决代码格式问题
def fixLeftAndEmpty(code):
    for i in range(0 , len(code)):
        code[i] = code[i].lstrip()
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


    filetools.writetxt(filename, "result", code)
    code = filetools.readCode(filename, "result")
    analize = filetools.checkstyle(filename,"result")

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
        print("检查规则" + analize[j])
        linecnt = int(analize[j].split(':')[2])
        print("行号=", linecnt, "CODE=",code[i])
        if i<linecnt-1:
            # result.append(code[i])
            i+=1
            continue
        #需要空行，默认为下2行
        if 'NeedBraces' in analize[j]:
            matches = analize[j].split('\'')
            print('matches=',matches)
            if matches[1] == 'else':
                cnt = code[i].index('else')
                strlist = list(code[i])
                strlist.insert(cnt+4,'{\n')
                code[i]="".join(strlist)
            else:
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
            for u in range(i,len(code)):
                flag = False
                pos = -1
                for v in range(0,len(code[u])):
                    if(code[u][v]==';' and v>0 and code[u][v-1]!='\\'):
                        flag = True
                        pos = v
                        break
                if flag:
                    strlist = list(code[u])
                    strlist.insert(pos+1,'\n}\n')
                    code[u]="".join(strlist)
                    break
        # print("修改后CODE=", code[i])
        j+=1

    #消除一下多余空格再重新写入
    filetools.writetxt(filename, "result", code)
    code = filetools.readCode(filename,"result")
    result = []
    for i in range(0,len(code)):
        code[i]=code[i].lstrip()
        if code[i]=='\n' or code[i]=='':
            continue
        else:
            result.append(code[i])
    code =result
    filetools.writetxt(filename, "result", code)
    code = filetools.readCode(filename, "result")
    analize = filetools.checkstyle(filename, "result")

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

        # print("检查规则"+analize[j])
        linecnt=int(analize[j].split(':')[2])
        # print("行号=",linecnt,"CODE=",code[i])

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
# TODO 修复BUG
#解决需求2的方法，输入为code[]，输出应为解决掉问题的code[]，作为下一步输出
def solveSecond(code,filename):
    # analize = filetools.checkstyle(filename,"result")
    file1 = open(os.path.join("words.txt"), 'r', encoding='UTF-8')
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
    sign = [' ', ',', ';', ':', '.','{', '}', '\n']
    # 注释问题
    keyword = ['abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'const', 'continue',
               'default', 'do', 'double', 'else', 'enum', 'extends', 'finally', 'float', 'for', 'goto', 'if',
               'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 'private',
               'protected', 'public', 'return', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized',
               'this', 'throw', 'throws', 'transient', 'try', 'void', 'volatile', 'while', 'println']
    base = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char', 'String']
    for codes in code:
        classflag = False
        constflag = False
        memberflag = False
        tmp = re.split('[ };,:{.\n]', codes)
        for i in tmp:
            #print("cas "+ i)
            if i == 'class':
                classflag = True
                constflag = False
                memberflag = False
            elif i == 'final':
                constflag = True
                classflag = False
                memberflag = False
            elif i in keyword:
                continue
            elif i in base:
                memberflag = True
                classflag = False
                constflag = False
            else:
                if len(i) == 0:
                    pass
                elif classflag:
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
        stringflag = False
        stringone = False
        tmpresult = ''
        i = 0
        while i < len(codes):
            if codes[i] == '"':
                stringflag = ~stringflag
                tmpresult += codes[i]
                i = i + 1
                continue
            if codes[i] == "'":
                stringone = ~stringone
                tmpresult += codes[i]
                i = i + 1
                continue
            if stringone or stringflag:
                tmpresult += codes[i]
                i = i + 1
                continue
            if (codes[i] == '"' and stringflag == False) or (codes[i] == "'" and stringone == False):
                tmpresult += codes[i]
                i = i + 1
                continue
            if codes[i] in sign:
                tmpresult += codes[i]
                i = i + 1
                continue
            tmp = (re.split('[ .;,{}\n]', codes[i:]))[0]
            i = i + len(tmp)
            if tmp in keyword or tmp in base:
                tmpresult += tmp
            elif tmp in constname:
                tmp1 = tmp.upper()
                tmpresult += tmp1
            elif tmp in classname:
                tmp1 = tmp[:1].upper() + tmp[1:].lower()
                for j in words:
                    index = tmp1.find(j)
                    if index != -1:
                        pass
                        tmp1 = tmp1.replace(j, j.title())
                        break
                tmpresult += tmp1
            elif tmp in membername:
                tmp1 = tmp.lower()
                for j in words:
                    index = tmp1.find(j)
                    if index == -1:
                        continue
                    tmp1 = tmp1.replace(j, j.title())
                    break
                tmpresult += tmp1
            else:
                tmpresult += tmp
        result.append(tmpresult)
    # for code in result:
        # print(code, end='')
    filetools.writetxt(filename, "result", result)
    return result

#我要找到后括号在啥子鬼地方
def findhkh(code, st, i):
    str=code[i].split(st,1)[0]+'}'
    i+=1
    while i<len(code):
        if re.match(str,code[i]):
            return i
        i+=1
    return -1

#解决需求3的方法，输入为code[]，输出应为解决掉问题的code[]，作为下一步输出
#TODO 实现本函数
def solveThird(code,filename,multiif_to_if,for_to_while,switch_to_if):
    base = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char', 'integer']
    print("3333333333sth  !!!   code:")
    multiif_to_if = -1
    for_to_while = -1
    switch_to_if = 1
    #0:不执行，1：正向过程，-1：逆向过程
    cur=0
    while cur < len(code):
        if code[cur]=='' or code[cur].strip()[0] == '/' :
            cur+=1
            continue

        if for_to_while==1:
            numkh=0
            numyh=0
            if re.match('for',code[cur].strip()):
                strtmp = code[cur].split('(', 1)
                strtmp.append(strtmp[1].rsplit(')', 1)[1])
                strtmp[1] = strtmp[1].rsplit(')', 1)[0]
                prechars = 'a'
                i = 0
                num = 0
                tjs = ['']
                while i < len(strtmp[1]):
                    if strtmp[1][i] == '(':
                        numkh += 1
                    if strtmp[1][i] == ')':
                        numkh -= 1
                    if strtmp[1][i] == '"' and prechars != '\\':
                        numyh += 1
                    if strtmp[1][i] == ';' and numkh == 0 and numyh % 2 == 0:
                        tjs.append('')
                        num += 1
                    else:
                        tjs[num] += strtmp[1][i]
                    i += 1
                print(tjs)
                j = findhkh(code,'for',cur)
                if tjs[0] != '':
                    code[cur] = tjs[0]+';\nwhile('+tjs[1]+')'
                else:
                    code[cur] = 'while('+tjs[1]+')'
                if '{' not in strtmp[2]:
                    code[cur]+=' {'
                if tjs[2] != '':
                    code[j] = tjs[2]+';'+code[j]
        elif for_to_while == -1:
            if re.match('while', code[cur].strip()):
                content = ['','','']
                content[1] = code[cur].split('(',1)[1].rsplit(')',1)[0]
                fx=code[cur-1].strip().split(' ')
                #注意！while转for是不可以把外面定义的变量拽进来的！因为定义域会变！可能导致错误！将来有空可以再来fix这部分，加检测。
                if (fx[0] in base) and fx[1] in content[1].split(' '):
                    #先扔着，原因如上！
                    print('yesyesyes')
                    j = findhkh(code,'while',cur)
                    if j-1!=cur and fx[1] in re.split('[ +-]',code[j-1]):
                        content[2] = code[j-1].rsplit(';',1)[0]
                        code[j-1]=''
                code[cur] = code[cur].split('while',1)[0]+'for('+content[0]+';'+content[1]+';'+content[2]+')'+code[cur].rsplit(')',1)[1]




        if multiif_to_if==1:
            numkh=0
            numyh=0
            if re.match('if',code[cur].strip()):
                strtmp = code[cur].split('(', 1)
                strtmp.append(strtmp[1].rsplit(')', 1)[1])
                strtmp[1] = strtmp[1].rsplit(')', 1)[0]
                prechars='a'
                i=0
                num=0
                tjs=['']
                while i<len(strtmp[1]):
                    if strtmp[1][i] == '(':
                        numkh+=1
                    if strtmp[1][i] == ')':
                        numkh-=1
                    if strtmp[1][i] == '"' and prechars!='\\':
                        numyh+=1
                    if strtmp[1][i]=='&' and numkh==0 and numyh%2==0:
                        tjs.append('')
                        num+=1
                        i+=1
                    else:
                        tjs[num]+=strtmp[1][i]
                    i+=1
                tmpresult=''
                for strs in tjs:
                    tmpresult+='if('+strs+')'
                tmpresult+=strtmp[2]
                code[cur]=tmpresult
        elif multiif_to_if==-1:
            if re.match('if', code[cur].strip()):
                if re.match('if',code[cur+1].strip()):
                    code[findhkh(code,'if',cur+1)]=''
                    code[cur+1]=code[cur].rsplit(')',1)[0]+' && '+code[cur+1].split('(',1)[1]
                    code[cur]=''
                elif re.match('{',code[cur+1].strip()) and re.match('if',code[cur+2].strip()):
                    code[findhkh(code, 'if', cur + 2)] = ''
                    code[cur + 2] = code[cur].rsplit(')', 1)[0] + ' && ' + code[cur + 2].split('(', 1)[1]
                    code[cur] = ''
                    code[cur+1] = ''
                    cur+=1


        cur+=1
    for codes in code:
        print(codes)
    #analize = filetools.checkstyle(filename,"result")
    return

