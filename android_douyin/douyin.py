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

def getUrl():
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
        getClipper2Txt.getDouyinUrl2Txt("out/douyi_rul.txt")
        time.sleep(0.5)