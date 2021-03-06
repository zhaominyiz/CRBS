
import os
import CodeRebuild.filetools as filetools
import re
from django.http import HttpResponse
"""
@author 马靖豪 赵珉怿 黄伟杰
@desc 本模块为代码重构系统的后端核心模块 分为3个小模块完成功能性需求
@date 2019/7/14
@copyright 南京理工大学 计算机科学与工程学院 剁椒鱼头队
说明：
classes:codetools()，具有hock(),solve(),getBlock(),fixLeftAndEmpty(),solveFirst(),solveSecond(),solveThird()方法

"""
"""
@author 赵珉怿
@desc 此函数为模板设计方法的内置钩子函数 子类可以根据自己的需求去改写此函数
@date 2019/7/14

@input code:输入修改之前的code代码数组
@output code:输出修改之后的code代码数组

"""


def hock(code):
    return code


"""
@author 赵珉怿
@desc 此函数为这个类的进入的函数，即模板方法的初始进入函数，定义了4步算法的基本操作
@date 2019/7/14

@input filename：文件名 multiif_to_if:多个if语句转一条if语句的需求 for_to_while：for语句转while语句的需求
switch_to_if：switch 语句转if语句的需求
@output filename:输出修改之后的文件名

"""


def solve(filename, multiif_to_if, for_to_while, switch_to_if):
    code = filetools.readCode(filename, "tmp")

    code = solveFirst(code, filename, False)
    for codes in code:
        print(codes)
    print("Step2")
    code = solveSecond(code, filename)

    for codes in code:
        print(codes)

    print("现在进入Step3")
    code = solveThird(code, filename, multiif_to_if, for_to_while, switch_to_if)
    print("STEP3结束")
    for cod in code:
        print(cod)

    code = solveFirst(code, filename, True)
    print("重构结束")
    code = hock(code)
    return filename


"""
@author 赵珉怿
@desc 此函数为返回固定格数空格的方法
@date 2019/7/12

@input cnt:想要空格的长度
@output str：cnt长度的空格

"""


def getBlock(cnt):
    str = ''
    for i in range(0, cnt):
        str += ' '
    return str


"""
@author 赵珉怿
@desc 此函数为消除函数左侧的留空
@date 2019/7/12

@input code:想要进行处理的代码
@output code：处理完毕的代码

"""


def fixLeftAndEmpty(code):
    for i in range(0, len(code)):
        code[i] = code[i].lstrip()
        flag = False
        # print(code[i], len(code[i]))
        j = 0
        while j < len(code[i]):

            if code[i][j] == '\"':
                flag = True
                j += 1
                continue
            if code[i][j] == '\"' and flag and code[i][j - 1] != '\\':
                flag = False
                j += 1
                continue
            if code[i][j] == ' ' and code[i][j + 1] == ' ' and flag == False:
                strlist = list(code[i])
                del strlist[j + 1]
                code[i] = "".join(strlist)
                j -= 1
            if code[i][j] == ' ' and code[i][j + 1] == ';' and flag == False:
                strlist = list(code[i])
                del strlist[j]
                code[i] = "".join(strlist)
                j -= 1

            j += 1
    return code


"""
@author 赵珉怿
@desc 此函数为流程的第一步，代码格式重构 进行添加' '、缩进、换行等功能
@date 2019/7/14

@input code：需要处理的代码数组 filename：代码的文件 noteflag：是否需要处理注释
@output code：进行处理后的代码数组

"""


def solveFirst(code, filename, noteflag):
    # 先去除左边的空格号
    code = fixLeftAndEmpty(code)
    # 再对一些语句进行换行的操作 如; 如循环语句
    for i in range(0, len(code)):
        # 标记引号和括号的个数 cnt%2==0 表示被引号包住了 cnt_k同理
        cnt = 0
        cnt_k = 0
        # 遍历code数组
        for j in range(0, len(code[i]) - 1):
            if code[i][j] == '"': cnt += 1
            if code[i][j] == '(' and cnt % 2 == 0:
                cnt_k += 1
            if code[i][j] == ')' and cnt % 2 == 0:
                cnt_k -= 1
            # 符合条件添加换行号
            if code[i][j] == ';' and cnt % 2 == 0 and code[i][j + 1] != '\n' and cnt_k == 0:
                strlist = list(code[i])
                strlist.insert(j + 1, '\n')
                code[i] = "".join(strlist)
            # 去除并判断 for while else 等语句
            if cnt % 2 == 0 and ((j + 2 < len(code[i]) and code[i][j] == 'f' and code[i][j + 1] == 'o' and code[i][
                j + 2] == 'r') or (
                                         j + 5 < len(code[i]) and code[i][j] == 'w' and code[i][j + 1] == 'h' and
                                         code[i][j + 2] and code[i][j + 3] == 'i'
                                         and code[i][j + 4] == 'l' and code[i][j + 5] == 'e') or (
                                         j + 3 < len(code[i]) and code[i][j] == 'e' and code[i][j + 1] == 'l'
                                         and code[i][j + 2] == 's' and code[i][j + 3] == 'e') or (
                                         j + 1 < len(code[i]) and code[i][j] == 'i' and code[i][j + 1] == 'f')):
                # 用于记录括号数
                cnt_ll = 0
                # 此标记用于判断是否已经进行断行操作，避免多余操作
                dealed = False
                if code[i][j] == 'e':
                    dealed = True
                    for u in range(j + 1, len(code[i]) - 1):
                        if code[i][u] == ' ':
                            if code[i][u + 1] != 'i':
                                strlist = list(code[i])
                                strlist.insert(u + 1, '\n')
                                code[i] = "".join(strlist)
                            break
                if dealed: continue
                # 用于找到括号右边的位置，进行断行
                for u in range(j + 1, len(code[i]) - 1):
                    if code[i][u] == '(' and code[i][u - 1] != '\\':
                        cnt_ll += 1
                    if code[i][u] == ')' and code[i][u - 1] != '\\':
                        cnt_ll -= 1
                        if cnt_ll == 0 and code[i][u + 1] != '\n':
                            strlist = list(code[i])
                            strlist.insert(u + 1, '\n')
                            code[i] = "".join(strlist)
                            break
                # print("FIN", code[i])
    # 写入到文件中 使得换行符发挥作用
    filetools.writetxt(filename, "result", code)
    # 再次读取到文件中
    code = filetools.readCode(filename, "result")

    # 再去除一行的多条语句
    for u in range(0, len(code)):
        # 标记匹配到的左括号数
        cntj = 0
        cntjj = 0
        flag = False
        for v in range(0, len(code[u])):
            if code[u][v] == '"':
                if v == 0 or code[u][v - 1] != '\\':
                    cntjj += 1
                    if cntjj % 2 == 1:
                        flag = True
            if flag:
                continue
            if code[u][v] == '(' and v > 0 and code[u][v - 1] != '\\':
                cntj += 1
            if code[u][v] == ')' and v > 0 and code[u][v - 1] != '\\':
                cntj -= 1
            if code[u][v] == ';' and v > 0 and code[u][v - 1] != '\\' and code[u][v + 1] != '\n' and cntj == 0:
                strlist = list(code[u])
                strlist.insert(v + 1, '\n')
                code[u] = "".join(strlist)
            # 处理一个单独的{
            if (code[u][v] == '}') and v > 0 and code[u][v - 1] != '\\':
                strlist = list(code[u])
                strlist.insert(v, '\n')
                code[u] = "".join(strlist)
            if (code[u][v] == '{') and v > 0 and code[u][v - 1] != '\\':
                strlist = list(code[u])
                strlist.insert(v + 1, '\n')
                code[u] = "".join(strlist)

            # 处理注释
            if (code[u][v] == '/' and v != len(code[u]) - 1 and code[u][v + 1] == '*') and v > 0 and code[u][
                v - 1] != '\\':
                strlist = list(code[u])
                strlist.insert(v + 2, '\n')
                code[u] = "".join(strlist)
                strlist = list(code[u])
                strlist.insert(v, '\n')
                code[u] = "".join(strlist)
            # 处理注释
            if (code[u][v] == '*' and v != len(code[u]) - 1 and code[u][v + 1] == '/'):
                strlist = list(code[u])
                strlist.insert(v + 2, '\n')
                code[u] = "".join(strlist)
                strlist = list(code[u])
                strlist.insert(v, '\n')
                code[u] = "".join(strlist)

    # 处理case 和 default的特殊情况
    for u in range(0, len(code)):
        if 'case' in code[u] or 'default' in code[u]:
            cnt_l = 0
            strlist = list(code[u])
            tmp = 0
            for v in range(0, len(code[u])):
                if code[u][v] == '"': cnt_l += 1
                if code[u][v] == ':' and code[u][v - 1] != '\\':
                    tmp = v
                    break
            if cnt_l % 2 == 0:
                strlist.insert(tmp + 1, '\n')
                code[u] = "".join(strlist)

    # print("!?!?")
    # for codes in code:
    #     print(codes)

    # 再次读入准备进行下一步操作
    filetools.writetxt(filename, "result", code)
    code = filetools.readCode(filename, "result")
    analize = filetools.checkstyle(filename, "result")

    # i 指的是代码的行数 j指的是分析的行数
    i = 0
    j = 1
    lazy = -1
    lazy2 = -1
    line_tag = 0

    # 再消除需要括号
    while True:
        # 若完了
        if i >= len(code) and j >= len(analize) - 1:
            break
        # 若报告扫到了最后
        if j >= len(analize) - 1:
            # result.append(code[i])
            i += 1
            continue
        # 获取行号 我们现在在分析第i+1行
        linecnt = int(analize[j].split(':')[2])
        # print("检查规则" + analize[j])
        linecnt = int(analize[j].split(':')[2])
        # print("行号=", linecnt, "CODE=",code[i])
        if i < linecnt - 1:
            # result.append(code[i])
            i += 1
            continue
        # 需要括号 进行扫描和处理，添加左括号和右括号
        if 'NeedBraces' in analize[j]:
            matches = analize[j].split('\'')
            # print('matches=', matches)
            if matches[1] == 'else':
                cnt = code[i].index('else')
                strlist = list(code[i])
                strlist.insert(cnt + 4, '{\n')
                code[i] = "".join(strlist)
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
                        strlist.insert(k + 1, '{\n')
                        code[i] = "".join(strlist)
                        break
            cnt_l = 0
            for u in range(i, len(code)):
                # print(code[u], "??", cnt_l)
                flag = False
                pos = -1
                cntl = 0
                for v in range(0, len(code[u])):
                    if code[u][v] == '(' and v > 0 and code[u][v - 1] != '\\':
                        cntl += 1
                    if code[u][v] == ')' and v > 0 and code[u][v - 1] != '\\':
                        cntl -= 1
                    if code[u][v] == '{' and (v > 0 or v == 0) and code[u][v - 1] != '\\':
                        cnt_l += 1
                    if code[u][v] == '}' and (v > 0 or v == 0) and code[u][v - 1] != '\\':
                        cnt_l -= 1
                    if ((code[u][v] == ';' or code[u][v] == '}') and (v > 0 or v == 0) and code[u][
                        v - 1] != '\\' and cntl == 0 and cnt_l == 1):
                        flag = True
                        pos = v
                        break
                if flag:
                    strlist = list(code[u])
                    strlist.insert(pos + 1, '\n}\n')
                    code[u] = "".join(strlist)
                    break
        # print("修改后CODE=", code[i])
        j += 1

    # 消除一下多余空格再重新写入
    filetools.writetxt(filename, "result", code)
    code = filetools.readCode(filename, "result")
    result = []
    for i in range(0, len(code)):
        code[i] = code[i].lstrip()
        if code[i] == '\n' or code[i] == '':
            continue
        else:
            result.append(code[i])
    code = result
    # print("F Result=")
    # for codes in code:
    #     print(codes)
    filetools.writetxt(filename, "result", code)
    code = filetools.readCode(filename, "result")
    analize = filetools.checkstyle(filename, "result")

    i = 0
    j = 1
    len_tag = -1
    exadd = 0
    record_w = -1
    # 用于记录上一层次空了几格

    while True:
        if i >= len(code) and j >= len(analize) - 1:
            break
        if j >= len(analize) - 1:
            i += 1
            continue

        # print("检查规则"+analize[j])
        linecnt = int(analize[j].split(':')[2])
        # print("行号=",linecnt,"CODE=",code[i])

        if i < linecnt - 1:
            # result.append(code[i])
            i += 1
            continue

        # 处理需要空格 记录这一行被处理了多少次此类事件
        if 'WhitespaceAround' in analize[j]:
            regex = r".*\'(.*)\'.*"
            matches = re.findall(regex, analize[j])
            # print('matches',matches)
            token = matches[0]
            wordcnt = int(analize[j].split(':')[3])
            tokenlen = len(token)

            strlist = list(code[i])
            lnull = len(code[i]) - len(code[i].lstrip())
            # print("LENTAG=", line_tag, "WORDCNT=", wordcnt, "EXADD=", exadd)
            if len_tag != linecnt:
                exadd = 0
            len_tag = linecnt
            if 'followed' in analize[j]:
                if record_w == wordcnt:
                    strlist.insert(wordcnt + lnull + tokenlen + exadd - 1, ' ')
                else:
                    strlist.insert(wordcnt + lnull + tokenlen + exadd - 1, ' ')
            else:
                if record_w == wordcnt:
                    strlist.insert(wordcnt + lnull + exadd - 2, ' ')
                else:
                    strlist.insert(wordcnt + lnull + exadd - 1, ' ')
            exadd += 1
            record_w = wordcnt
            code[i] = "".join(strlist)
        j += 1

    # 处理缩进
    # print("处理缩进~~")
    # i 指着code j指着分析
    tapnum = [0] * (len(code) + 2)
    for j in range(1, len(analize) - 1):
        # print("!???")
        # print(analize[j])
        linecnt = int(analize[j].split(':')[2])
        # print(analize[j])
        if 'Indentation' in analize[j]:
            regex = r'.*应为(.*)个.*'
            matches = re.findall(regex, analize[j])
            # print(matches)
            tapct = int(matches[0])
            tapct *= 2
            tapnum[linecnt - 1] = tapct
        if '[CommentsIndentation]' in analize[j]:
            regex = r'.*第(.*)行.*'
            matches = re.findall(regex, analize[j])
            # print(matches)
            tapct = int(matches[0])
            # print("FROM", i, "TO", tapct)
            for u in range(i, tapct):
                tapnum[u] = tapnum[0 if i - 1 == -1 else i - 1]
    for i in range(0, len(code)):
        if code[i][0] == '@':
            tapnum[i + 1] = max(tapnum[i + 1], tapnum[i])
    # tapnum[len(code)-1]=0
    st = -1
    ed = -1
    # 看看是不是需要处理注释部分
    if noteflag:
        for i in range(0, len(code)):
            if code[i][0] == '/' and code[i][1] == '*':
                st = i
            if code[i] == '*/\n':
                ed = i
                tapnum[st] = 0 if st - 1 == -1 else tapnum[st - 1]
                for u in range(st, ed + 1):
                    tapnum[u] = tapnum[st]
                # code[st] = code[st][:-1]+'*\n'
                # for u in range(st+1, ed+1):
                #     code[u]=' * '+code[u]
    for i in range(0, len(code)):
        str = getBlock(tapnum[i])
        # print("此行应当缩进",tapcnt)
        code[i] = str + code[i]
        # print(code[i])
    filetools.writetxt(filename, "result", code)
    code = filetools.readCode(filename, "result")
    for i in range(0, len(code)):
        if i > 0 and code[i][0] == '/':
            code[i] = getBlock(1 * (len(code[i - 1]) - len(code[i - 1].lstrip()))) + code[i]
        elif code[i][0] == 'b' and code[i][1] == 'r' and code[i][2] == 'e' and code[i][3] == 'a' and code[i][4] == 'k':
            code[i] = getBlock(1 * (len(code[i - 1]) - len(code[i - 1].lstrip()))) + code[i]

    filetools.writetxt(filename, "result", code)
    return filetools.readCode(filename, "result")


"""
@author 黄伟杰
@desc 此函数为流程的第二步，代码类名变换
@date 2019/7/14

@input code：需要处理的代码数组 filename：代码的文件 
@output code：进行处理后的代码数组

"""
def solveSecond(code, filename):
    # analize = filetools.checkstyle(filename,"result")
    # 常用字字典的读取
    file1 = open(os.path.join("words.txt"), 'r', encoding='UTF-8')
    words = []
    line = file1.readline()
    while line:
        line = file1.readline()
        words.append(line[:line.__len__() - 1])
        # words.append("'"+line+"'")
    file1.close()

    keyword = []
    # JAVA关键字字典的读取
    file1 = open('keywords.txt', 'r', encoding='UTF-8')
    line = file1.readline()
    while line:
        line = file1.readline()
        keyword.append(line[:line.__len__() - 1])
    file1.close()

    # print(keyword)
    # words.append('banana')
    # print(words)
    # 存储变量名，类名，常量名，方法名
    membername = []
    classname = []
    constname = []
    methonname = []
    nochange = []
    result = []
    # 对应的修改或的变量名等
    dict = {}
    zhushi = False
    # 逐行处理代码 进行类型分析 不进行修改
    for codes in code:
        len = codes.__len__()
        first = True
        tmpresult = ''
        classflag = False
        constflag = False
        memberflag = False
        dotflag = False
        first = True
        i = 0
        while i < len:
            # 如果是变量名
            if (codes[i] >= 'a' and codes[i] <= 'z') or (codes[i] >= 'A' and codes[i] <= 'Z') \
                    or (codes[i] == '_') or codes[i] == '$':
                tmpword = ''
                while i < codes.__len__() - 1 and (
                        (codes[i] >= 'a' and codes[i] <= 'z') or (codes[i] >= 'A' and codes[i] <= 'Z') \
                        or (codes[i] >= '0' and codes[i] <= '9') or (codes[i] == '_') or codes[i] == '$'):
                    tmpword += codes[i]
                    i = i + 1
                # 已经是一个类名了
                if tmpword in classname:
                    continue
                # class表示后面将声明一个类
                if tmpword == 'class':
                    classflag = True
                    first = False
                    constflag = False
                    continue
                # final 表示后面声明一个常量
                elif tmpword == 'final':
                    constflag = True
                    classflag = False
                    first = False
                    continue
                # 如果此时的词是一个java关键词
                elif tmpword in keyword or first:
                    memberflag = True
                    first = False
                    continue
                elif classflag == True:
                    classname.append(tmpword)
                    tmp1 = tmpword[:1].upper() + tmpword[1:].lower()
                    # 在常用字词典进行查询
                    for j in words:
                        index = tmp1.find(j)
                        if index != -1:
                            pass
                        tmp1 = tmp1.replace(j, j.title())
                    dict[tmpword] = tmp1
                    # 常量则进行全部大写
                elif constflag == True:
                    constname.append(tmpword)
                    dict[tmpword] = tmpword.upper()
                elif memberflag == True:
                    membername.append(tmpword)
                    tmp1 = tmpword.lower()
                    # 变量名通过常用字词典进行驼峰命名法
                    for j in words:
                        index = tmp1[1:].find(j)
                        if index == -1:
                            continue
                        tmp1 = tmp1.replace(j, j.title())
                    dict[tmpword] = tmp1
                # 判断是否为方法名
                elif codes[i] == '(':
                    tmp1 = tmpword.lower()
                    for j in words:
                        index = tmp1[1:].find(j)
                        if index == -1:
                            continue
                        tmp1 = tmp1.replace(j, j.title())
                    dict[tmpword] = tmp1
                    methonname.append(tmpword)
                elif first == True:
                    memberflag = True
            else:
                i = i + 1
    # 逐行读取，依据上面的额标志进行修改
    for codes in code:
        len = codes.__len__()
        first = True
        tmpresult = ''
        classflag = False
        constflag = False
        memberflag = False
        dotflag = False
        i = 0
        # 处理注释问题
        while i < len:
            if zhushi == True:
                while i < len:
                    tmpresult += codes[i]
                    # 多行注释问题
                    if i > 0 and codes[i] == '/' and codes[i - 1] == '*':
                        zhushi = False
                        i = i + 1
                        break
                    i = i + 1
                    # 处理字符串问题
            elif codes[i] == '"':
                tmpresult += codes[i]
                i = i + 1
                while codes[i] != '"':
                    tmpresult += codes[i]
                    i = i + 1
                tmpresult += codes[i]
                i = i + 1
                continue
            # 处理当行注释
            elif i + 1 < len and codes[i] == '/' and codes[i + 1] == '/':
                while i < len:
                    tmpresult += codes[i]
                    i = i + 1
            elif dotflag == True:
                while i < codes.__len__() - 1 and (
                        (codes[i] >= 'a' and codes[i] <= 'z') or (codes[i] >= 'A' and codes[i] <= 'Z') \
                        or (codes[i] >= '0' and codes[i] <= '9') or (codes[i] == '_') or codes[i] == '$'):
                    tmpresult += codes[i]
                    i = i + 1
                dotflag = False
            elif (codes[i] >= 'a' and codes[i] <= 'z') or (codes[i] >= 'A' and codes[i] <= 'Z') or codes[i] == '_' or \
                    codes[i] == '$':
                tmpword = ''
                while i < codes.__len__() - 1 and (
                        (codes[i] >= 'a' and codes[i] <= 'z') or (codes[i] >= 'A' and codes[i] <= 'Z') \
                        or (codes[i] >= '0' and codes[i] <= '9') or (codes[i] == '_') or codes[i] == '$'):
                    tmpword += codes[i]
                    i = i + 1
                # 判断此时词语所属的类型 且进行相应的变化
                # 已经存在对应的字典里
                if tmpword in keyword:
                    tmpresult += tmpword
                elif tmpword in classname:
                    tmpresult += dict[tmpword]
                elif tmpword in methonname:
                    tmpresult += dict[tmpword]
                elif tmpword in constname:
                    tmpresult += dict[tmpword]
                elif tmpword in membername:
                    tmpresult += dict[tmpword]
                else:
                    tmpresult += tmpword
            else:
                tmpresult += codes[i]
                if i > 0 and codes[i] == '*' and codes[i - 1] == '/':
                    zhushi = True
                i = i + 1
        result.append(tmpresult)
    # 调试输出
    # print(classname)
    # print(constname)
    # print(membername)
    # filetools.writetxt(filename, "result", result)
    return result



"""
@author 马靖豪
@desc 此函数为找到一行语句后面的花括号是在什么位置
@date 2019/7/14

@input code：需要处理的代码数组 st：行号 i：行号的单词号
@output code：进行处理后的代码数组

"""
def findhkh(code, st, i):
    str = code[i].split(st, 1)[0] + '}'
    i += 1
    while i < len(code):
        if re.match(str, code[i]):
            return i
        i += 1
    return -1


"""
@author 马靖豪
@desc 此函数为流程的第三步，用于解决各种语句互转的问题
@date 2019/7/14

@input code：需要处理的代码数组 filename：代码的文件 
multiif_to_if：是否需要将多if语句和一条if语句互相转换
for_to_while：是否需要将for语句while语句互相转换
switch_to_if：是否需要将switch和if语句互相转换
@output code：进行处理后的代码数组

"""


def solveThird(code, filename, multiif_to_if, for_to_while, switch_to_if):
    # 类型
    base = ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char', 'integer']
    base2 = ['byte', 'short', 'int', 'char', 'String']
    basemp = []
    # 用于switch case记录变量
    tokens = {}
    token = {}
    print("3333333333sth  !!!   code:")
    # 0:不执行，1：正向过程，-1：逆向过程
    cur = 0
    # 分析语法
    while cur < len(code):
        if code[cur] == '' or code[cur].strip()[0] == '/':
            cur += 1
            continue

        strtmp = code[cur].strip().split(' ', 1)
        if strtmp[0] in base2:
            basemp.append(strtmp[1].split('=|;')[0])
        # for to while
        if for_to_while == 1:
            numkh = 0
            numyh = 0
            if re.match('for', code[cur].strip()):
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
                if num != 2:
                    cur += 1
                    continue
                j = findhkh(code, 'for', cur)
                if tjs[0] != '':
                    code[cur] = tjs[0] + ';\nwhile(' + tjs[1] + ')' + strtmp[2]
                else:
                    code[cur] = 'while(' + tjs[1] + ')' + strtmp[2]

                if '{' not in strtmp[2]:
                    code[cur] += '\n{'
                if tjs[2] != '':
                    code[j] = tjs[2] + ';\n' + code[j]
        # while to for
        elif for_to_while == -1:
            if re.match('while', code[cur].strip()):
                content = ['', '', '']
                content[1] = code[cur].split('(', 1)[1].rsplit(')', 1)[0]
                fx = code[cur - 1].strip().split(' ')
                # 注意！while转for是不可以把外面定义的变量拽进来的！因为定义域会变！可能导致错误！将来有空可以再来fix这部分，加检测。
                if (fx[0] in base) and fx[1] in content[1].split(' '):
                    # 先扔着，原因如上！
                    print('yesyesyes')
                    j = findhkh(code, 'while', cur)
                    if j - 1 != cur and fx[1] in re.split('[ +-]', code[j - 1]):
                        content[2] = code[j - 1].rsplit(';', 1)[0]
                        code[j - 1] = ''
                code[cur] = code[cur].split('while', 1)[0] + 'for(' + content[0] + ';' + content[1] + ';' + content[
                    2] + ')' + code[cur].rsplit(')', 1)[1]
        # multiif to if
        if multiif_to_if == 1:
            numkh = 0
            numyh = 0
            if re.match('if', code[cur].strip()):
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
                    if strtmp[1][i] == '&' and numkh == 0 and numyh % 2 == 0:
                        tjs.append('')
                        num += 1
                        i += 1
                    else:
                        tjs[num] += strtmp[1][i]
                    i += 1
                tmpresult = ''
                for strs in tjs:
                    tmpresult += 'if(' + strs + ')\n'
                tmpresult += strtmp[2]
                code[cur] = tmpresult
        # if to multiif
        elif multiif_to_if == -1:
            if re.match('if', code[cur].strip()):
                if re.match('if', code[cur + 1].strip()):
                    code[findhkh(code, 'if', cur + 1)] = ''
                    code[cur + 1] = code[cur].rsplit(')', 1)[0] + ' && ' + code[cur + 1].split('(', 1)[1]
                    code[cur] = ''
                elif re.match('{', code[cur + 1].strip()) and re.match('if', code[cur + 2].strip()):
                    code[findhkh(code, 'if', cur + 2)] = ''
                    code[cur + 2] = code[cur].rsplit(')', 1)[0] + ' && ' + code[cur + 2].split('(', 1)[1]
                    code[cur] = ''
                    code[cur + 1] = ''
                    cur += 1

        cur += 1
        # switch to if
        if switch_to_if == 1:
            if re.match('switch', code[cur].strip()):
                token[code[cur].split('switch', 1)[0] + '    '] = code[cur].split('(', 1)[1].rsplit(')', 1)[0]
                en = findhkh(code, 'switch', cur)
                code[cur] = '{'
                if re.match('{', code[cur + 1].strip()):
                    code[cur + 1] = ''
                # code[en]=''
            elif re.match('case', code[cur].strip()):
                if tokens[code[cur].split('case', 1)[0] + '  '] == '':
                    tokens[code[cur].split('case', 1)[0] + '  '] += token[code[cur].split('case', 1)[0] + '  '] + '==' + \
                                                                    code[cur].split('(', 1)[1].rsplit(')', 1)[0]
                else:
                    tokens[code[cur].split('case', 1)[0] + '  '] += '||' + token[
                        code[cur].split('case', 1)[0] + '  '] + '==' + code[cur].split('(', 1)[1].rsplit(')', 1)[0]
                code[cur] = '}\nif(' + tokens[code[cur].split('case', 1)[0] + '  '] + ')\n{'
            elif re.match('break;', code[cur].strip()):
                tmp = code[cur].split('break;', 1)[0]
                tokens[tmp] = ''
                while not (re.match('case', code[cur + 1].strip()) and code[cur + 1].split('case', 1)[0] + '  ' == tmp):
                    code[cur] = ''
                    cur += 1
        # if to switch
        elif switch_to_if == -1:
            if re.match('if', code[cur].strip()):
                en = findhkh(code, 'if', cur)

    for codes in code:
        print(codes)
    filetools.writetxt(filename, "result", code)
    # analize = filetools.checkstyle(filename,"result")
    return code