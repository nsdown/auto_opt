# -*- coding: utf-8 -*-
'''
@ Copyright (C) 2018        EfonFighting(email:efonfighting@126.com)(android_wechat:Efon-fighting)
@
@ env stetup：
@ sudo apt install tesseract-ocr 下载chi_sim.traineddata 放到/usr/share/tesseract-ocr/4.00/tessdata
(windows安装完后需要配置PATH,然后下载chi_sim.traineddata 放到C:\Program Files (x86)\Tesseract-OCR\tessdata),
@ pip3 install pillow pytesseract matplotlib aircv opencv-python
@
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

def getEssay(fileName, isToButtom):
    '''
    @ 获取公众号所有历史文章，入口。
    @
    @ return
    @
    @ param
    @ exception
    @ notice
    @   需要安装app : https://github.com/majido/clipper
    '''
    getEssaytimeStart = datetime.datetime.now()
    flgPos = None
    adb.dumpDeviceInfo()
    box = {'x1':0, 'y1':170, 'x2':500, 'y2':382} #目标标题的范围
    boxDeltaY = box['y2'] - box['y1']
    startTopicCnt = 3   #最开始在目标标题范围之下的标题个数+1
    adb.runAdbCmd('shell am startservice ca.zgrs.clipper/.ClipboardService') #开启粘贴板adb通信service

    #-> 滑动到底部
    if(isToButtom):
        scrollToButtom()

    while True:
        fh = open(fileName, 'a+', encoding='utf-8')
        timeStart = datetime.datetime.now()
        capPath = 'out/screencap.png'
        capPathXSize = 720
        capPathYSize = 1280

        #保证滑动到位---start---
        while True:
            adb.pullScreenShot(capPath)
            FlgYList = getFlgFromPicVir(capPathXSize-20, capPath)
            if(len(FlgYList) < 2):
                adb.adbSwipe(box['x1'], box['y1'], box['x1'], box['y1'] + 20, 300, 0)  # 实测4个像素点
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
                    timeDelta = (getEssaytimeEnd - getEssaytimeStart).seconds
                    print('Total time: ' + str(int(timeDelta / 3600)) + 'h' + str(int(timeDelta / 60) % 60) + 'm' + str((timeDelta % 60)) + 's')  # 时间差

                    fh.close()
                    exit(0)
                else:
                    adb.adbSwipe(box['x1'], box['y1'], box['x1'], box['y1'] + 20, 300, 0)  # 实测4个像素点
                    print(FlgYList)
                    print('slite 1:------------------------------------------------------')
            elif((abs(scrollDelta1) < 6) & (abs(scrollDelta2) < 6)): #通过高度卡目标区域，获取到目标区域，读图
                break
            else: # 没滑动到位，继续一点一点往下滑动补偿，直到到位
                adb.adbSwipe(box['x1'], box['y1'], box['x1'], box['y1'] + 20, 300, 0) #实测4个像素点
                print(FlgYList)
                print('slite 2:------------------------------------------------------')
        # 保证滑动到位---end---

        text = getTextFromPic(capPath, box['x1'], box['y1']+startTopicCnt*boxDeltaY,
                                        box['x2'], box['y2']+startTopicCnt*boxDeltaY)

        adb.adbTap((box['x1'] + box['x2'])/2,(box['y1'] + box['y2'])/2+startTopicCnt*boxDeltaY) #进入文章

        flgPos = adb.FindFlgFromCap('android_wechat/flag_pic/00_dot_option.png',0.85, True, 2) # 等待文章加载2s
        adb.adbTap(flgPos[0], flgPos[1])
        flgPos = None

        flgPos = adb.FindFlgFromCap('android_wechat/flag_pic/00_cp_link.png', 0.85, True, 0)
        adb.adbTap(flgPos[0], flgPos[1])
        flgPos = None

        # 获取网址---start---
        textLink = adb.runAdbCmd('shell am broadcast -a clipper.get') #获取粘贴板内容
        textLinkList = textLink.split('data=',3)
        textLink = textLinkList[len(textLinkList)-1].strip('\n').strip('"') #strip方法用于移除字符串头尾指定的字符（默认为空格）。
        print(textLink)
        # 获取网址---end---

        adb.runAdbCmd('shell input keyevent KEYCODE_BACK') # [bug]存在偶现不起作用的问题
        time.sleep(1) #反应时间

        fh.write(text + ' : ' + textLink + '\n')

        if(startTopicCnt != 0): #保证底部几个都被读取到
            startTopicCnt -= 1
        else:
            adb.adbSwipe(box['x1'], box['y1'], box['x1'], box['y2'] + scrollOffsite, 1000, 0)

        fh.close()
        timeEnd = datetime.datetime.now()
        print("Take time:" + str((timeEnd-timeStart).seconds) + "s") #时间差

    getEssaytimeEnd = datetime.datetime.now()
    timeDelta = (getEssaytimeEnd - getEssaytimeStart).seconds
    print('Total time: ' + str(int(timeDelta / 3600)) + 'h' + str(int(timeDelta / 60) % 60) + 'm' + str((timeDelta % 60)) + 's')  # 时间差

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
                     CapXSize / 2, CapYSize / 5, 100, 3) # 反应时间3s，否则可能一直加载不出来

        if(adb.FindFlgFromCap('android_wechat/flag_pic/00_no_more.png', 0.8, False, 0) != None):
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
    filePath = 'out/screencap.png'
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
        if((grey.getpixel((x,y)) >= 229) and (grey.getpixel((x,y)) <= 232)):
            yList.append(y) #添加列表项
    return yList

def showImg():
    img = Image.open('out/screencap.png')
    grey = img.convert('L')
    plt.imshow(grey)
    plt.show()