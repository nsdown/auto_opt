#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
'''
@ Copyright (C) 2018        EfonFighting(email:efonfighting@126.com)(wechat:Efon-fighting)
@
@ env stetup：
@  sudo apt-get install python3-pip
@
'''

def main():
    print("main start.")
    caseFlg = 'url2pdf'
    print(caseFlg)

    if(caseFlg == 'getEssay'):
        from wechat import get_gzh_essay
        get_gzh_essay.getEssay()

    if (caseFlg == 'url2pdf'):
        from url2pdf import url2pdf
        url2pdf.url2pdf("wechat/小路超车.txt")

if __name__ == "__main__":  #这里可以判断，当前文件是否是直接被python调用执行
    main()

