# -*- coding: utf-8 -*-
# __Author__='Zhangbo'
# __Time__='2018/8/21 15:41'

import os

rootdir = 'D:/PycharmProjects/PythonScript\自动化测试框架/case_result/2018-07-10_17-58-41/log'
list = os.listdir(rootdir)

auth="no_shutdown_"
'''
分析日志的模块，查找日志中标志性信息产生的次数
'''
#定义你需要查找的对象的正则表达式wordcheck
#需要分析的日志的路径filesource
def checklog(wordcheck,filesource):
    print(filesource.split("/")[-1])
    #定义一个空的字典用来存放查询的结果
    size={}
    #异常捕获当文件不存在的时候抛出异常
    try:
        #打开日志文件
        file=open(filesource,"r",encoding='utf-8',errors='ignore')
        #循环读取日志文件的每一行
        for i in file:
            # print(i)
            #使用re模块的search功能查找当前行是否能和正则匹配
            if wordcheck in i:
                print(i)
                # x=re.search(wordcheck,i)
            #如果匹配到结果则执行if中的代码
            # if x:
            #     #取出查询到的结果
            #     tmp=x.group()
            #     #get函数作用是如果字典中取不到key的值则赋一个默认值，也就是每一次查询到一个新的结果就将这个结果作为key vlaue=0新加到字典中
            #     size[tmp]=size.get(tmp,0)
            #     #在字典中将value加1，记录一次查找
            #     size[tmp]+=1
        #关闭文件
        file.close()
    #如果有异常抛出文件异常
    except FileExistsError as e:
        print(e)
    #没有异常打印结果
    else:
        return size
#测试分析apache访问日志中的所有访问过的ip和次数
for x in list:
    y=rootdir+"/"+x
    checklog("Shutting down VM",y)


