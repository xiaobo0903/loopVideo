# -*- coding: UTF-8 -*-
''' 
**********************************************************************************************
COPYRIGHT (C), Sunshine Cloud Video . Co., Ltd.  
File NAME:  pubTools.py
Author:  xiaobo      
Version: v1.0   
Date:  2020-09-16 
DESCRIPTION: channel Manager Executor Class                         
Others: None
**********************************************************************************************          
'''
import time  # 引入time模块
import subprocess
import re
import log as mylog
import myglobal as mygl

class chExecutor:
    channel_id = 0
    channel_type = ""
    cmd = "ffmpeg"

    def __init__(self, channel_id, channel_type):

        self.channel_id = channel_id
        self.channel_type = channel_type
    
    #本线程的工作
    def  channel_Thread_Running(self):
        #判读全局变量中是否存在本频道的数据，如果没有本频道的内容，则停止该线程
        while True:
            ret = mygl.get_value(self.channel_id)
            if not ret:
                self.kill_FFmpeg_pid()
                break
            time.sleep(1)
            mylog.logger.debug("the channel_id["+str(self.channel_id)+"] thread is running......")
        mylog.logger.debug("the channel_id["+str(self.channel_id)+"] thread is stoped!")
    #按频道id取机器ffmpeg进程的列表
    def get_FFmpeg_pid(self):
        #ffmpeg -re -i 0106wjxw.mp4 -c copy -f flv rtmp://localhost/loopvideo/1 -metadata title="[loopvideo_channel_id:123]"
        plist = []
        retl = None
        command = "ps -a opid,cmd|grep ffmpeg|grep -v grep"
        t1 = time.time()
        ret = subprocess.getoutput(command)

        if ret == '':
            return plist

        retl = ret.split("\n") #按回车分割成数组
        mylog.logger.debug("ps -ef:\n"+ret)
        for line in retl:
            res = re.findall("^(\d+).*loopvideo_channel_id:"+str(self.channel_id), line)#
            if len(res) == 0:
                continue
            plist.append(res[0])
        t2 = time.time() - t1
        return plist

    #杀掉ffmpeg指定的进程；
    def kill_FFmpeg_pid(self):
        
        plist = self.get_FFmpeg_pid()
        if not plist:
            return
        
        for r in plist:
            command = "kill -9 "+r
            ret = subprocess.getoutput(command)

if __name__ == "__main__":
    ce = chExecutor(123, "live")
    ce.channel_Thread_Running()
