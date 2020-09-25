# -*- coding: UTF-8 -*-
''' 
**********************************************************************************************
COPYRIGHT (C), Sunshine Cloud Video . Co., Ltd.  
File NAME:  pubTools.py
Author:  xiaobo      
Version: v1.0   
Date:  2020-09-16 
DESCRIPTION: loopVideo Server Public Tools Class                         
Others: None
**********************************************************************************************          
'''
import time  # 引入time模块
import hashlib

md5 = hashlib.md5()

#获取系统时间，此为本地时间；格式为:yyyymmdd hhMMss 并返回两个整型数；
def getSysDataTimeStr():

    t = time.time()
    lt = time.localtime(t)
    str_c = time.strftime("%Y%m%d %H%M%S", lt)
    dt = str_c.split()
    return int(dt[0]), int(dt[1]), int(t)

#取当前的时间，返回的是微秒 1秒=1000000微秒
def getTimeStamp():
    t = time.time()
    return int(round(t * 1000000))       