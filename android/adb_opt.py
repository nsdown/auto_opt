# -*- coding: utf-8 -*-
'''
@ Copyright (C) 2018        EfonFighting(email:efonfighting@126.com)(wechat:Efon-fighting)
@
@ env stetup：
@  pip3 install aircv opencv-python
@  pip3 install numpy
@  sudo apt install python3-tk
@
'''
import os
import sys
import subprocess
import platform
import aircv as ac
import cv2

class AdbOpt():
    def __init__(self):
        '''
        @ adb   工具类初始化，检查adb路径与环境
        @
        @ return
        @
        @ param
        @ exception
        @ notice
        '''
        self.deviceIdList = {'Mate9':'3HX0217601006195',
                             }
        self.deviceId = '' #创建类之后需要赋值 deviceId
        if platform.system() == 'Windows':
            adbToolPath = os.path.join("adb")
            self.option = ''
        elif platform.system() == 'Linux':
            adbToolPath = '/home/soy/Android/Sdk/platform-tools/adb'
            self.option = ' -s ' + self.deviceId
        else:
            print('Host OS is not compatible.\n')
            exit(1)

        print('adbToolPath:' + adbToolPath)
        try:
            subprocess.Popen(
                [adbToolPath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.adbToolPath = adbToolPath
        except OSError:
            print('请安装 ADB 及驱动并配置环境变量')
            exit(1)

    def testDevice(self):
        '''
        @ 查看是否有设备连接
        @
        @ return
        @
        @ param
        @ exception
        @ notice
        '''
        print('检查设备是否连接...')
        commandList = [self.adbToolPath, 'devices']
        process = subprocess.Popen(commandList, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.communicate()
        print('adb 输出:')
        #self.deviceId[0] = print(output[0].decode('utf8').replace('\n\n', '').split('\n', 8)[1].split('	',8)[0])
        for each in output:
            print(each.decode('utf8').replace('\n\n', ''))

        if output[0].decode('utf8') == 'List of devices attached\n\n':
            print('未找到设备，请连接设备后重试。')
            exit()
        else:
            print('设备已连接...')

    def getScreenSize(self):
        '''
        @ adb 获取屏幕分辨率
        @
        @ return    屏幕分辨率（eg. "Physical size: 1080x1920 Override size: 720x1280"）
        @
        @ param
        @ exception
        @ notice
        '''
        process = os.popen(self.adbToolPath + self.option +' shell wm size')
        output = process.read()
        return output

    def getScreenDensity(self):
        '''
        @ 获取屏幕DPI（每英寸点数）
        @
        @ return
        @
        @ param
        @ exception
        @ notice
        '''
        process = os.popen(self.adbToolPath + self.option +' shell wm density')
        output = process.read()
        return output

    def getDeviceInfo(self):
        '''
        @ 获取ro.product.device
        @
        @ return
        @
        @ param
        @ exception
        @ notice
        '''
        process = os.popen(self.adbToolPath + self.option +' shell getprop ro.product.device')
        output = process.read()
        return output

    def getDeviceOsInfo(self):
        '''
        @ 获取ro.build.version.release
        @
        @ return
        @
        @ param
        @ exception
        @ notice
        '''
        process = os.popen(self.adbToolPath + self.option +' shell getprop ro.build.version.release')
        output = process.read()
        return output

    def dumpDeviceInfo(self):
        '''
        @ 检查设备连接状态，显示设备信息
        @
        @ return
        @
        @ param
        @ exception
        @ notice
        '''
        self.testDevice()
        deviceIdStr = self.deviceId
        sizeStr = self.getScreenSize()
        deviceStr = self.getDeviceInfo()
        phoneOSStr = self.getDeviceOsInfo()
        densityStr = self.getScreenDensity()
        print(
"""********** 设备信息 开始 **********
deviceName      :{device}
deviceId        :{deviceId}
screenSize      :{size}
DPI             :{dpi}
Phone OS        :{phone_os}
Host OS         :{host_os}
Python          :{python}
********** 设备信息 结束**********""".format(
            deviceId=deviceIdStr,
            size=sizeStr.replace('\n', ' '),
            dpi=densityStr.replace('\n', ' '),
            device=deviceStr.replace('\n', ' '),
            phone_os=phoneOSStr.replace('\n', ' '),
            host_os=sys.platform.replace('\n', ' '),
            python=sys.version.replace('\n', ' '),)
        )

    def getScreenCapSize(self):
        '''
        @ adb 获取截屏图片分辨率
        @
        @ return  eg.[720,1280]
        @
        @ param
        @ exception
        @ notice
        '''
        process = os.popen(self.adbToolPath + self.option +' shell wm size')
        output = process.read().replace(' ', '').replace('\n', '').split(':')
        x = output[len(output)-1].split('x')[0]
        y = output[len(output)-1].split('x')[1]
        size = [int(x),int(y)]
        return size

    def runAdbCmd(self, rawCommand):
        '''
        @ 执行任意adb命令
        @
        @ return
        @
        @ param
        @ exception
        @ notice
        '''
        command = '{} {}'.format(self.adbToolPath, rawCommand)
        process = os.popen(command)
        output = process.read()
        return output

    def pullScreenShot(self, savePath):
        '''
        @ 获取屏幕截图
        @
        @ return
        @
        @ param
        @ exception
        @ notice
        '''
        #print(savePath)
        self.runAdbCmd('shell screencap -p /sdcard/screencap.png')
        self.runAdbCmd('pull /sdcard/screencap.png ' + savePath)
        return savePath

    def adbTap(self, x, y):
        '''
        @ 单击任意坐标点(x,y)
        @
        @ return
        @
        @ param
        @ exception
        @ notice
        '''
        cmd = 'shell input tap {x} {y}'.format(
            x=x,
            y=y,
        )
        print(cmd)
        self.runAdbCmd(cmd)

    def adbSwipe(self, x1, y1, x2, y2, ms):
        '''
        @ 从一点滑动到另一点
        @
        @ return
        @
        @ param
        @ exception
        @ notice
        '''
        cmd = 'shell input swipe {x1} {y1} {x2} {y2} {ms}'.format(
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
            ms=ms,
        )
        print(cmd)
        self.runAdbCmd(cmd)

    def drawCircle(self, img, pos):
        '''
        @ 在任意坐标点(x,y)画圆
        @
        @ return
        @
        @ param
        @ exception
        @ notice
        '''
        circleRadius = 50
        color = (0, 155, 0)
        line_width = 5
        cv2.circle(img, pos, circleRadius, color, line_width)
        cv2.imshow('screenshot', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def FindFlgFromCap(self, flgPath, confidenceVTH):
        '''
        @ 在图片中找出特征图案
        @
        @ return 特征图案中心坐标(x,y) or None
        @
        @ param
        @    confidenceVTH:0.0-1.0
        @ exception
        @ notice    必须像素点匹配
        '''
        process = os.popen('date +%m%d%H%M%S')
        date = process.read().replace('\n','')
        date = '' #不保存时间戳
        screenshotPath = self.pullScreenShot('screen_cap/screencap'+date+'.png') # eg. screen_cap/cap1006120638.png
        print(screenshotPath)
        imsrc = ac.imread(screenshotPath)
        imdst = ac.imread(flgPath)
        pos = ac.find_template(imsrc, imdst)
        if ((pos != None) and (pos['confidence'] > confidenceVTH)):
            print('find a {para1}:{para2}'.format(para1=flgPath,para2=pos))
            flgCenterPosInt = (int(pos['result'][0]), int(pos['result'][1]))
            # draw_circle(imsrc, circleCenterPosInt)  # draw circle
            #str(input('确定开始下一步？[y/n]:'))
            return flgCenterPosInt
        else:
            print('Do not find {para1}\n'.format(para1=flgPath))
            return None

    def tapFlgFromPic(self, flgPath, confidenceVTH):
        '''
        @ 单击图片中的特征图案
        @
        @ return True/False
        @
        @ param
        @ exception
        @ notice    必须像素点匹配
        '''
        flgCenterPosInt = self.FindFlgFromPic(flgPath, confidenceVTH)
        if (flgCenterPosInt != None):
            self.adbTap(flgCenterPosInt[0], flgCenterPosInt[1])
            return True
        else:
            return False