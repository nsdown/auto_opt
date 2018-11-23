# -*- coding: utf-8 -*-
'''
@ Copyright (C) 2018        EfonFighting(email:efonfighting@126.com)(android_wechat:Efon-fighting)
@
@ env stetup：
@
@ 0.screenSize:960 * 540 DPI:320
@ 1.打开抖音主页 -> 点开开始采集的视频
@
'''
from android import getClipper2Txt
from android.adb_opt import adbIns
import time


def getDouyinUrl2Txt(saveFilePath):
    '''
     @ 获取douyin app视频“标题-->描述-->地址”
     @
     @ return str
     @
     @ param
     @ exception
     @ notice
     '''
    fileLine = '%05d' % (len(open(saveFilePath, 'r', encoding='utf-8').readlines()) + 1)
    fh = open(saveFilePath, 'a+', encoding='utf-8')

    textLink = getClipper2Txt.getClipper()
    textLink = textLink.split('#在抖音，记录美好生活#',5)[1].split('复制此链接',5)[0].strip()
    textLink = textLink.replace(" http","-->http").strip()
    textLink = textLink.replace("@抖音小助手","").strip()
    print(textLink)
    fh.write(fileLine + "-->" + textLink + '\n')

    fh.close()
    print('getDouyinUrl2Txt ok.')

def getUrl():
    '''
     @ 不断往下滑，依次点击“复制链接”
     @
     @ return clipper
     @
     @ param
     @ exception
     @ notice
     @      每步操作之间用延时处理，复制链接时要求：网速好，系统流畅；
     '''
    #adbIns.pullScreenShot('screen_cap')
    print('press any key to start...')
    input()
    while True:
        print('--- 开始获取 ---')
        #input()
        adbIns.adbSwipe(100, 600, 100, 30, 500)
        time.sleep(0.3)
        adbIns.tapFlgFromPic('android_douyin\pic_flag\share.png',0.75)
        time.sleep(1)
        adbIns.adbSwipe(500, 800, 10, 800, 500)
        time.sleep(0.3)
        adbIns.tapFlgFromPic('android_douyin\pic_flag\cp_link.png', 0.75)
        time.sleep(1)
        getDouyinUrl2Txt("out/douyi_rul.txt")
        time.sleep(0.5)