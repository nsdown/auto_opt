#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
'''
@ Copyright (C) 2018        EfonFighting(email:efonfighting@126.com)(wechat:Efon-fighting)
@
@ env stetup：
@ sudo apt install tesseract-ocr
@ pip3 install pillow pytesseract matplotlib
@ 需要安装app : https://github.com/majido/clipper
@ 0.screenSize:720x1280 DPI:320
@ 1.打开微信公众号 -> 历史消息界面
@
'''
import matplotlib.pyplot as plt
from android.adb_opt import AdbOpt
import pytesseract
from PIL import Image
import datetime
import time

deviceName = 'Mate9'
scrollOffsiteList = {'Mate9':7, #实际滑动的损失像素个数补偿，经验统计值，允许不够，后面再进一步补偿
                    }

adb = AdbOpt()
adb.deviceId = adb.deviceIdList[deviceName]
scrollOffsite = scrollOffsiteList[deviceName]
CapXSize = adb.getScreenCapSize()[0]
CapYSize = adb.getScreenCapSize()[1]

def getEssay():
    '''
    @ 获取公众号所有历史文章，入口。
    @
    @ return
    @
    @ param
    @ exception
    @ notice
    '''
    getEssaytimeStart = datetime.datetime.now()
    flgPos = None
    adb.dumpDeviceInfo()
    box = {'x1':0, 'y1':170, 'x2':500, 'y2':382} #目标标题的范围
    boxDeltaY = box['y2'] - box['y1']
    startTopicCnt = 3   #最开始再目标标题范围之下的标题个数+1
    adb.runAdbCmd('shell am startservice ca.zgrs.clipper/.ClipboardService') #开启粘贴板adb通信service

    #-> 滑动到底部
    scrollToButtom()

    fh = open('wechat/get_gzh_essay_result'+ '' +'.txt', 'w+', encoding='utf-8')
    while True:
        timeStart = datetime.datetime.now()
        capPath = 'screen_cap/screencap.png'
        capPathXSize = 720
        capPathYSize = 1280

        #保证滑动到位---start---
        while True:
            adb.pullScreenShot(capPath)
            FlgYList = getFlgFromPicVir(capPathXSize-20, capPath)
            if(len(FlgYList) < 2):
                adb.adbSwipe(box['x1'], box['y1'], box['x1'], box['y1'] + 20, 300)  # 实测4个像素点
                print(FlgYList)
                print('slite 3:------------------------------------------------------')
                continue

            scrollDelta1 = box['y1'] - FlgYList[0]
            scrollDelta2 = box['y2'] - FlgYList[1]
            if(FlgYList[0] > capPathYSize/2): #第一条线过半屏幕，到顶退出
                textEnd = getTextFromPic(capPath, box['x1'], (FlgYList[0] - (box['y2'] - box['y1'])),
                                      box['x2'], FlgYList[0] )
                if(textEnd[0:4] == '历史消息'):
                    print('getEssay End.')
                    getEssaytimeEnd = datetime.datetime.now()
                    print('Total time: ' + (getEssaytimeEnd - getEssaytimeStart).seconds)  # 时间差
                    fh.close()
                    exit(0)
                else:
                    adb.adbSwipe(box['x1'], box['y1'], box['x1'], box['y1'] + 20, 300)  # 实测4个像素点
                    print(FlgYList)
                    print('slite 1:------------------------------------------------------')
            elif((abs(scrollDelta1) < 6) & (abs(scrollDelta2) < 6)): #通过高度卡目标区域，获取到目标区域，读图
                break
            else: # 没滑动到位，继续一点一点往下滑动补偿，直到到位
                adb.adbSwipe(box['x1'], box['y1'], box['x1'], box['y1'] + 20, 300) #实测4个像素点
                print(FlgYList)
                print('slite 2:------------------------------------------------------')
        # 保证滑动到位---end---

        text = getTextFromPic(capPath, box['x1'], box['y1']+startTopicCnt*boxDeltaY,
                                        box['x2'], box['y2']+startTopicCnt*boxDeltaY)

        adb.adbTap((box['x1'] + box['x2'])/2,(box['y1'] + box['y2'])/2+startTopicCnt*boxDeltaY) #进入文章

        while(flgPos == None): #等待界面出现
            time.sleep(1)
            flgPos = adb.FindFlgFromCap('wechat/flag_pic/00_dot_option.png',0.85)
        adb.adbTap(flgPos[0], flgPos[1])
        flgPos = None

        while (flgPos == None): #等待界面出现
            time.sleep(1)
            flgPos = adb.FindFlgFromCap('wechat/flag_pic/00_cp_link.png', 0.85)
        adb.adbTap(flgPos[0], flgPos[1])
        flgPos = None

        # 获取网址---start---
        textLink = adb.runAdbCmd('shell am broadcast -a clipper.get') #获取粘贴板内容
        textLinkList = textLink.split('data=',3)
        textLink = textLinkList[len(textLinkList)-1].strip('\n').strip('"') #strip方法用于移除字符串头尾指定的字符（默认为空格）。
        print(textLink)
        # 获取网址---end---

        time.sleep(1)  # 反应时间
        adb.runAdbCmd('shell input keyevent KEYCODE_BACK') # 存在偶现不起作用的问题
        time.sleep(1) #反应时间

        fh.write(text + ' : ' + textLink + '\n')

        if(startTopicCnt != 0): #保证底部几个都被读取到
            startTopicCnt -= 1
        else:
            adb.adbSwipe(box['x1'], box['y1'], box['x1'], box['y2'] + scrollOffsite, 1000)

        timeEnd = datetime.datetime.now()
        print((timeEnd-timeStart).seconds) #时间差

    fh.close()

    getEssaytimeEnd = datetime.datetime.now()
    timeDelta = (getEssaytimeEnd - getEssaytimeStart).seconds
    print('Total time(s): ' + str(int(timeDelta / 3600)) + 'h' + str(int(timeDelta / 60) % 60) + 'm' + str((timeDelta % 60)) + 's')  # 时间差

def scrollToButtom():
    '''
    @ 滑动到底部
    @
    @ return
    @
    @ param
    @ exception
    @ notice
    '''
    adb.pullScreenShot('')
    while True:
        adb.adbSwipe(CapXSize / 2, CapYSize * 4 / 5,
                     CapXSize / 2, CapYSize / 5, 100)
        if(adb.FindFlgFromCap('wechat/flag_pic/00_no_more.png', 0.8) != None):
            print('scroll to end OK.')
            break

def getTextFromPic(filePath, x1, y1, x2, y2):
    '''
    @ 从图片的特定区域识别出文字
    @
    @ return
    @
    @ param
    @ exception
    @ notice
    '''
    img = Image.open(filePath)
    grey = img.convert('L')
    cutPic = grey.crop((x1, y1, x2, y2))

    xSize = cutPic.size[0]
    ySize = cutPic.size[1]
    for y in range(ySize):
        for x in range(xSize):
            if(cutPic.getpixel((x,y)) != 255):
                cutPic.putpixel((x,y),0)

    itemStr = pytesseract.image_to_string((cutPic), lang='chi_sim').replace(' ', '')
    itemStrList = itemStr.split('\n',8)
    dateStr = itemStrList[len(itemStrList)-1]
    topicStr = ''
    for idx in range (len(itemStrList)-1):
        topicStr += itemStrList[idx]
    print(dateStr+'_'+topicStr)
    return(dateStr+'_'+topicStr)

    if False:
        plt.imshow(img)
        plt.show()

def getTextFromScreen(x1, y1, x2, y2):
    '''
    @ 从屏幕上的特定区域识别出文字
    @
    @ return
    @
    @ param
    @ exception
    @ notice
    '''
    filePath = 'screen_cap/screencap.png'
    adb.pullScreenShot(filePath)
    return getTextFromPic(filePath, x1, y1, x2, y2)

def getFlgFromPicVir(x, filePath):
    '''
    @ 在图片上的(垂直方向)找(特定亮度值)的点
    @
    @ return 特定点的垂直坐标值list
    @
    @ param
    @ exception
    @ notice
    '''
    img = Image.open(filePath)
    grey = img.convert('L')
    ySize = grey.size[1]
    if False: #for debug
        plt.imshow(grey)
        plt.show()

    yList = [] #空列表
    for y in range(ySize):
        if(grey.getpixel((x,y)) == 229):
            yList.append(y) #添加列表项
    return yList

def showImg():
    img = Image.open('screen_cap/screencap.png')
    grey = img.convert('L')
    plt.imshow(grey)
    plt.show()