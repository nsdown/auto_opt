# -*- coding: utf-8 -*-
'''
@ Copyright (C) 2018        EfonFighting(email:efonfighting@126.com)(android_wechat:Efon-fighting)
@
@ description: 读取鼠标在屏幕中的坐标，并显示。
@
@ env stetup：
@   pip install pyautogui
@
'''

import os,time
import pyautogui as pag

def getPointAxis():
    try:
        while True:
                print ("Press Ctrl-C to end")
                x,y = pag.position() #返回鼠标的坐标
                posStr="Position:"+str(x).rjust(4)+','+str(y).rjust(4)
                print (posStr)#打印坐标
                time.sleep(0.2)
                os.system('clear')#清除屏幕
    except  KeyboardInterrupt:
        print ('end....')



"""
附录：鼠标模拟和键盘模拟的范例。
pip install PyUserInput
################模拟鼠标
from pymouse import *
m = PyMouse()
m.click(1806, 14)
m.click(x,y,button,n) #鼠标点击;x,y 是坐标位置;button #1表示左键，2表示点击右键;n –点击次数，默认是1次，2表示双击
m.click(577, 490, 1)

################鼠标事件监控
class Clickonacci(PyMouseEvent):
  def __init__(self):
    PyMouseEvent.__init__(self)

  def click(self, x, y, button, press):
    print(time.time(), button, press)

c = Clickonacci()
c.run()

###############模拟键盘
from pykeyboard import *
k = PyKeyboard()
k.type_string(u'杀毒防御') # 我靠不能输入中文啊。。。
k.press_key('H') # 模拟键盘按H键
k.release_key('H') # 模拟键盘松开H键
k.tap_key('H') # 模拟点击H键
k.tap_key('H', n=2, interval=5) # 模拟点击H键，2次，每次间隔5秒
k.tap_key(k.function_keys[5]) # 点击功能键F5

###############组合键模拟
#例如同时按alt+tab键盘
k.press_key(k.alt_key) # 按住alt键
k.tap_key(k.tab_key) # 点击tab键
k.release_key(k.alt_key) # 松开alt键

###############键盘事件监听
class TapRecord(PyKeyboardEvent):
  def __init__(self):
    PyKeyboardEvent.__init__(self)

  def tap(self, keycode, character, press):
    print(time.time(), keycode, character, press)

t = TapRecord()
t.run()

"""