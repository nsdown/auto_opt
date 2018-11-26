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


def saveDouyinUrl2Txt(saveFilePath):
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

def getUrl(savePath):
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
        saveDouyinUrl2Txt(savePath)
        time.sleep(0.5)

def getVideoFromTxt(txtPath, startLine, endLine):
    '''
    @ 解析txt字段，在浏览器下载无水印视频
    @
    @ return null
    @
    @ param
    @ exception
    @ notice
    @
    '''
    __browser_url = r'C:\Users\soy\AppData\Roaming\360se6\Application\360se.exe'  ##360浏览器的地址
    chrome_options = Options()
    chrome_options.binary_location = __browser_url
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get("http://douyin.iiilab.com/")
    time.sleep(3) # 经验值，根据网速调整

    cnt = 0
    for line in open(txtPath, encoding='utf-8'):
        cnt = cnt + 1
        print(line)
        if ((cnt < startLine) | (cnt > endLine) | (len(line.split('-->')) != 3)): # 容错
            continue

        inputUrl = driver.find_element_by_class_name('link-input') # 输入框
        inputUrl.send_keys(line.split('-->', 4)[2])
        time.sleep(0.5)

        analysisBtn = driver.find_element_by_class_name('input-group-btn') # 解析按钮
        analysisBtn.click()
        time.sleep(4)

        downloadBtn = driver.find_element_by_class_name('btn-success')  # 下载按钮
        urlSite = downloadBtn.get_attribute('href')
        print(urlSite)
        urllib.request.urlretrieve(urlSite, filename='C:\\Users\\soy\\Downloads\\%s.mp4' % line.split('-->', 4)[0], reporthook=None, data=None)
        print('download %s.mp4 ok' % line.split('-->', 4)[0])
        time.sleep(1)

def uploadVideo2qQunmin(urlTxtPath, videoPath, stardIdx, endIdx):
    '''
    @ 上传视频到
    @
    @ return null
    @
    @ param
    @ exception
    @ notice
    @   需要先打开全民小视频首页，
    @   需要安装ADBKeyboard.app支持adb中文输入
    '''
    print('uploadVideo start.')
    adbIns.runAdbCmd('shell ime set com.android.adbkeyboard/.AdbIME') #切换输入法
    pushVideo_quanmin_axis = (270, 930) # 全民小视频发视频按钮
    selectVideo_quanmin_axis = (450, 880) # 选视频按钮
    firstVideo_quanmin_axis = (65, 250) # 选取第一个视频
    nextStep1_quanmin_axis = (480, 800) # 下一步
    nextStep2_quanmin_axis = (450, 880) # 下一步
    describe_quanmin_axis = (200, 200) # 视频描述
    fabu_quanmin_axis = (260, 810) # 发布

    for idx in range(stardIdx, endIdx):
        IdxName = ('%03d' % idx)
        print("push %s/%s.mp4 /sdcard/Movies/quanmin.mp4" % (videoPath, IdxName))
        adbIns.runAdbCmd("push %s/%s.mp4 /sdcard/Movies/quanmin.mp4" % (videoPath, IdxName))
        #adbIns.runAdbCmd("push %s/002.mp4 /sdcard/Movies" % (videoPath))
        adbIns.adbTap(pushVideo_quanmin_axis[0], pushVideo_quanmin_axis[1])
        time.sleep(2)
        adbIns.adbTap(selectVideo_quanmin_axis[0], selectVideo_quanmin_axis[1])
        time.sleep(2)
        adbIns.adbTap(firstVideo_quanmin_axis[0], firstVideo_quanmin_axis[1])
        time.sleep(2)
        adbIns.adbTap(nextStep1_quanmin_axis[0], nextStep1_quanmin_axis[1])
        time.sleep(2)
        adbIns.adbTap(nextStep2_quanmin_axis[0], nextStep2_quanmin_axis[1])
        time.sleep(2)
        adbIns.adbTap(describe_quanmin_axis[0], describe_quanmin_axis[1])
        time.sleep(1)
        adbIns.adbTap(describe_quanmin_axis[0], describe_quanmin_axis[1])

        # 获取描述
        urlTxtFd = open(urlTxtPath, 'r', encoding='utf-8')
        lineTemps = urlTxtFd.readlines()
        for lineTemp in lineTemps:
            if (lineTemp.find(IdxName) != -1):
                describeText = lineTemp.split('-->',5)[1]
                print(IdxName + ':' + describeText)
                adbIns.runAdbCmd("shell am broadcast -a ADB_INPUT_TEXT --es msg %s" % (describeText))
                break

        time.sleep(20)
        adbIns.adbTap(fabu_quanmin_axis[0], fabu_quanmin_axis[1])
        time.sleep(10)

    adbIns.runAdbCmd('shell ime set com.android.adbkeyboard/.AdbIME')  # 切换为讯飞输入法