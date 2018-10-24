# -*- coding: utf-8 -*-
'''
@ Copyright (C) 2018        EfonFighting(email:efonfighting@126.com)(wechat:Efon-fighting)
@
@ env stetup：
@
'''
from linux_pc import virtkey_func
import time
import webbrowser
import datetime


def url2pdfLinux(filePath, startLine, endLine):
    '''
    @ 通过(title : url)文档打印为pdf文档
    @
    @ return
    @
    @ param
    @ exception
    @ notice 默认浏览器需要为firefox
    '''
    url2pdfStart = datetime.datetime.now()
    cnt = 0
    for line in open(filePath):
        cnt = cnt + 1
        if ((cnt < startLine) | (cnt > endLine)):
            continue

        webbrowser.open(line.split(' : ', 2)[1])
        virtkey_func.tapPageDownToEnd() #让图片缓冲出来
        time.sleep(2) # 让网页缓冲完成

        virtkey_func.tapCtrlChar('p') # ctrl+p

        # rename pdf titile
        virtkey_func.tapTab()
        virtkey_func.tapTab()
        virtkey_func.tapEnter()
        virtkey_func.enterStr(line.split(' : ', 2)[0])
        virtkey_func.tapEnter()

        # print start
        virtkey_func.tapTab()
        virtkey_func.tapTab()
        virtkey_func.tapTab()
        virtkey_func.tapEnter()
        time.sleep(8)
        virtkey_func.tapEnter() # 如果重名冲突，按替换再打印（可优化）
        time.sleep(8)

        # 关闭browser
        virtkey_func.tapCtrlChar('w')

    #统计耗时
    url2pdfEnd = datetime.datetime.now()
    timeDelta = (url2pdfEnd - url2pdfStart).seconds
    print('Total time: ' + str(int(timeDelta / 3600)) + 'h' + str(int(timeDelta / 60) % 60) + 'm' + str((timeDelta % 60)) + 's')   # 时间差