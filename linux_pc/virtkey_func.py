#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
'''
@ Copyright (C) 2018        EfonFighting(email:efonfighting@126.com)(android_wechat:Efon-fighting)
@
@ env stetup：
@  virtkey : https://launchpad.net/virtkey (sudo python3.6 setup.py install)
@
'''

import virtkey
import pyperclip
import time

tapTime = 0.5

def tapEnter():
    v = virtkey.virtkey()  # 调用系统键盘
    v.press_keysym(65421) # enter
    v.release_keysym(65421)
    time.sleep(tapTime)

def tapCtrlChar(char):
    v = virtkey.virtkey()  # 调用系统键盘
    v.press_keysym(65507)  # Ctrl键位
    v.press_unicode(ord(char))  # 模拟字母V
    v.release_unicode(ord(char))
    v.release_keysym(65507)
    time.sleep(tapTime)

def tapTab():
    v = virtkey.virtkey()  # 调用系统键盘
    v.press_keysym(65289) # Tab
    v.release_keysym(65289)
    time.sleep(tapTime)

def enterStr(stringVal):
    pyperclip.copy(stringVal)
    tapCtrlChar('v')
    time.sleep(tapTime)

def tapPageDownToEnd():
    v = virtkey.virtkey()  # 调用系统键盘
    for i in range(20):
        v.press_keysym(65366)
        v.release_keysym(65366)
        time.sleep(tapTime)

'''
keysym	.keycode	.keysym_num	Key
			
Alt_L	64	65513	左手边的Alt键
			
Alt_R	113	65514	右手边的Alt键
			
BackSpace	22	65288	BackSpace
			
Cancel	110	65387	Pause Break
			
Caps_Lock	66	65549	CapsLock
			
Control_L	37	65507	左手边的Control键
			
Control_R	109	65508	右手边的Control键
			
Delete	107	65535	Delete
			
Down	104	65364	方向键：下
			
End	103	65367	End
			
Escape	9	65307	Esc
			
Execute	111	65378	系统调用
			
F1	67	65470	F1
			
F2	68	65471	F2
			
Fi	66+i	65469+i	Fi
			
F12	96	68481	F12
			
Home	97	65360	Home
			
Insert	106	65379	Insert
			
Left	100	65361	方向键：左
			
Linefeed	54	106	Linefeed（Ctrl-j）
			
KP_0	90	65438	数字键：0
			
KP_1	87	65436	数字键：1
			
KP_2	88	65433	数字键：2
			
KP_3	89	65435	数字键：3
			
KP_4	83	65430	数字键：4
			
KP_5	84	65437	数字键：5
			
KP_6	85	65432	数字键：6
			
KP_7	79	65429	数字键：7
			
KP_8	80	65431	数字键：8
			
KP_9	81	65434	数字键：9
			
KP_Add	86	65451	运算键：+
			
KP_Begin	84	65437	小键盘：5号键
			
KP_Decimal	91	65439	“.”键
			
KP_Delete	91	65439	Delete
			
KP_Divide	112	65455	“/”键
			
KP_Down	88	65433	方向键：下
			
KP_End	87	65436	End
			
KP_Enter	108	65421	Enter
			
KP_Home	79	65429	Home
			
KP_Insert	90	65438	Insert
			
KP_Left	83	65430	方向键：左
			
KP_Multiply	63	65450	运算键：*
			
KP_Next	89	65435	PageDown
			
KP_Prior	81	65434	PageUp
			
KP_Right	85	65432	方向键：右
			
KP_Subtract	82	65453	“-”键
			
KP_Up	80	65431	方向键：上
			
Next	105	65366	PageDown
			
Num_Lock	77	65407	NumLock
			
Pause	110	65299	Pause
			
Print	111	65377	PrintScreen
			
Prior	99	65365	PageUp
			
Return	36	65293	回车键
			
Right	102	65363	方向键：右
			
Scroll_Lock	78	65300	ScrollLock
			
Shift_L	50	65505	左手边的Shift键
			
Shift_R	62	65506	有手边的Shift键
			
Tab	23	65289	Tab
			
Up	98	65362	方向键：上
			
    
'''