# -*- coding: utf-8 -*-

from android.adb_opt import AdbOpt

def getUrl2Txt():
    adb = AdbOpt()
    adb.runAdbCmd('shell am startservice ca.zgrs.clipper/.ClipboardService')  # 开启粘贴板adb通信service
    fh = open("out/douyi_rul.txt", 'a+', encoding='utf-8')
    while True:
        print('按"enter"复制粘贴板内容到PC本地文件；按 q 退出。。。')
        str = input()
        print(str)
        if str == 'a':
            textLink = adb.runAdbCmd('shell am broadcast -a clipper.get')  # 获取粘贴板内容
            textLinkList = textLink.split('data=', 3)
            textLink = textLinkList[len(textLinkList) - 1].strip('\n').strip('"')  # strip方法用于移除字符串头尾指定的字符（默认为空格）。
            print(textLink)
            fh.write(textLink + '\n')
        if str == 'q':
            print('退出。。')
            break

    fh.close()