# -*- coding: utf-8 -*-
'''
@ Copyright (C) 2018        EfonFighting(email:efonfighting@126.com)(android_wechat:Efon-fighting)
@
@ env stetup：
@   sudo apt-get install python3-pip
@
'''

def main():
    print("main start")
    caseFlg = 'url2pdf'
    print(caseFlg)

    if (caseFlg == 'douyin'):
        from android_douyin import douyin
        urlTxtPath = "/home/soy/03_autoOpt_docs/douyin_Ina.txt"
        douyin.getUrlFromDouyin(urlTxtPath)
        #douyin.getVideoFromTxt("out/douyin_Sia.txt", 1, 80)
        #douyin.uploadVideo2Qunmin('/home/soy/Videos/sihaiweijiazaiouzhou/sihaiweijiazaiouzhou.txt',
        #                          '/home/soy/Videos/sihaiweijiazaiouzhou',26, 29)


    if(caseFlg == 'getPointAxis'):
        from pc_windows import screen_coordinate
        screen_coordinate.getPointAxis()

    if(caseFlg == 'getEssay'):
        from android_wechat import get_gzh_essay
        get_gzh_essay.getEssay('out/laodongfaku.txt',False)

    if (caseFlg == 'url2pdf'):
        from url2pdf import url2pdf
        url2pdf.url2pdfLinux("out/laodongfaku.txt", 101, 10000)


def test():
    import time
    # 获取描述
    urlTxtFd = open('out/抖音_四海为家在欧洲.txt', 'r', encoding='utf-8')
    lineTemps = urlTxtFd.readlines()
    for lineTemp in lineTemps:
        findRet = lineTemp.find('005')
        print(findRet)
        if(findRet != -1):
            print(lineTemp)
        time.sleep(1)


if __name__ == "__main__":  #这里可以判断，当前文件是否是直接被python调用执行
    main()
    #test()

