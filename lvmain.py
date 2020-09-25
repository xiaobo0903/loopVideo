# -*- coding: UTF-8 -*-
''' 
**********************************************************************************************
COPYRIGHT (C), Sunshine Cloud Video . Co., Ltd.  
File NAME:  wloopvideo.py
Author:  xiaobo      
Version: v1.0   
Date:  2020-09-16 
DESCRIPTION: loopvideo Web Server                          
服务的主类：每五秒轮询一次频道表，对于频道表的内容进行更新处理，如果频道表存在，则放入到系统的全局变量channl_list中；
每个线程会读取该全局数据，如果没有查询到自已线程的channel_list，则删除本线程建立的ffmpeg进程， 线程通出；
**********************************************************************************************          
'''

import time  # 引入time模块
import myexc
import json
import myglobal as mygl
import time
import log as mylog
import threading
import chexecutor

mygl._myinit("./setting.conf") #需要先于myexc进行初始化；
mygl._init()    #初始化内存变量

#from table(channel),get channel info;
def getMyChannel():

    mydb = myexc.myExc()
    qstr = "select channel_id, channel_type from channel where status = 'normal'"
    new_jch = mydb.queryToJson(qstr)
    gl_ch = mygl.get_dict()
    d_ch = []
    for ch_key in gl_ch:
        channel_id = ch_key
        #判断channel_id记录是否在新记录中存在；
        isExit = False
        for nr in new_jch:
            #如果原来的频道在新记录中不存在，则需要删除该频道；
            channel_id1 = nr["channel_id"]
            if channel_id == channel_id1:
                isExit = True
                break
        if not isExit:
            d_ch.append(channel_id)#删除后该处理的线程会自动停止,因为在iteration状态下不能够删除key，所以需要中间使用数组过渡处理

    for nk in d_ch:
        gl_ch.pop(nk)
        mylog.logger.debug("delete a channel: channel_id:"+str(nk))

    for r2 in new_jch:
        channel_id = r2["channel_id"]
        val = r2["channel_type"]
        if channel_id not in gl_ch:    #如果新记录中的频道，在老记录中不存在，则需要增加该频道的处理线程；
            gl_ch[channel_id] = r2["channel_type"]
            mylog.logger.debug("need start a new thread: channel_id:"+str(channel_id)+" channel_type:"+str(r2["channel_type"]))
            t = threading.Thread(target=channel_thread, args=(channel_id, r2["channel_type"],))
            t.start()
            continue
        if val == r2["channel_type"]:
            continue
        else:
            mylog.logger.debug("need start a modify thread.........")

    mylog.logger.debug("the data is :"+str(gl_ch))
    mylog.logger.debug("the global data is :"+str(mygl.get_dict()))
    mylog.logger.debug("the main thread is begin sleep 5 seconds......")
    time.sleep(20)
    mylog.logger.debug("the main thread is starting ......")

#频道的主线程
def channel_thread(channel_id, channel_type):

    chex = chexecutor.chExecutor(channel_id, channel_type)
    chex.channel_Thread_Running()
    mylog.logger.debug("the "+str(channel_id)+" thread is starting ......")

if __name__ == '__main__':
    while True:
        getMyChannel()