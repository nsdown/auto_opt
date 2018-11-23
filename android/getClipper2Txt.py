# -*- coding: utf-8 -*-

from android.adb_opt import adbIns

def getClipper():
    '''
    @ 获取android手机粘贴板内容
    @
    @ return str
    @
    @ param
    @ exception
    @ notice
    '''
    adbIns.runAdbCmd('shell am startservice ca.zgrs.clipper/.ClipboardService')  # 开启粘贴板adb通信service
    textLink = adbIns.runAdbCmd('shell am broadcast -a clipper.get')  # 获取粘贴板内容
    textLinkList = textLink.split('data=', 3)
    textLink = textLinkList[len(textLinkList) - 1].strip('\n').strip('"')  # strip方法用于移除字符串头尾指定的字符（默认为空格）。
    return textLink