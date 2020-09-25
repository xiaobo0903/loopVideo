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
import pubtools
import myexc
import myglobal as mygl

class chExecutor:
    
    mydb = None
    channel_id = 0
    channel_type = ""
    idate = 0        #当前的日期
    cmd = "ffmpeg"
    m_url = ""   #当前播放的视频流地址，如果不一样，则需要启动该内容；
    m_type = ""  #当前的媒体的流类型，file 和 live

    def __init__(self, channel_id, channel_type):

        self.channel_id = channel_id
        self.channel_type = channel_type
        self.mydb = myexc.myExc()
    
    #本线程的工作
    def  channel_Thread_Running(self):
        #判读全局变量中是否存在本频道的数据，如果没有本频道的内容，则停止该线程
        while True:
            ret = mygl.get_value(self.channel_id)   #获取当前频道状态是否正常
            if not ret:     #获取当前频道状态是否正常，如果频道被删除，则需要杀死进程，然后退出；
                self.kill_FFmpeg_pid()
                break
            self.cur_Media_Confirm()   #确认当前的媒体内容，如果当前的拉流的媒体不是现在的媒体内容，则停止拉流；
            self.ensure_Channel_Pid()  #如果当前的频道没有启动，则需要启动该频道的内容；
            time.sleep(1)
            mylog.logger.debug("the channel_id["+str(self.channel_id)+"] thread is running......")
        mylog.logger.info("the channel_id["+str(self.channel_id)+"] thread is stoped!")

    #保证频道的拉流进程，正常运行，如果没有运行，则需要启动拉流进程；
    def ensure_Channel_Pid(self):
        ret = self.get_FFmpeg_pid()
        if not ret:
            #需要启动线程的工作；
            cmd = "nohup ffmpeg"
            if self.m_type == "file":
                cmd = "ffmpeg -re"    #如果是文件类型，则需要加入re参数；
            
            #判读m_url是否为hls的格式，如果以http开头，则认为是hls格式，在拉取hls流时，需要增加:-bsf:a aac_adtstoasc参数
            bsf_str = ""
            if ".m3u8" in self.m_url:
                bsf_str = "-bsf:a aac_adtstoasc"

            cmd = cmd + " -i "+self.m_url+" -c copy "+bsf_str+" -f flv rtmp://localhost/loopvideo/"+str(self.channel_id)+" -metadata title=\"loopvideo_channel_id:"+str(self.channel_id)+"\">/dev/null 2>&1&"
            subprocess.call(cmd, shell=True)

    #当前频道，媒体内容的确认，如果库中媒体内容与运行的内容相同，则保持现状，如果不同，则杀掉该运行的进程；        
    def cur_Media_Confirm(self):

        idate, itime, curtime = pubtools.getSysDataTimeStr()
        self.idate = idate
        itime = itime
        curtime = curtime
        sql = sql = "select media_type, media_url from program where channel_id = "+str(self.channel_id)+" and status = 'normal' and isloop = 0 and lv_date = "+str(self.idate)+" and start_time <=  "+str(itime)+" and end_time>= "+str(itime)+" limit 1"
        
        result  = self.mydb.queryToJson(sql)
        if len(result) == 0:
            self.getBackProgramUrl()
            return

        if result[0]["media_url"] == self.m_url:
            return
        else:
            self.m_type = result[0]["media_type"]
            self.m_url = result[0]["media_url"]
            self.kill_FFmpeg_pid()  #杀死当前的ffmpeg处理进程

    #取当前频道的背景直播文件;
    def getBackProgramUrl(self):

        sql = "select media_type, media_url from program where channel_id = "+str(self.channel_id)+" and status = 'normal' and isloop = 1 and lv_date = "+str(self.idate)+" limit 1"
        result  = self.mydb.queryToJson(sql)
        if len(result) == 0:
            return
        if result[0]["media_url"] == self.m_url:
            return
        else:
            self.m_type = result[0]["media_type"]
            self.m_url = result[0]["media_url"]
            self.kill_FFmpeg_pid()  #杀死当前的ffmpeg处理进程

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
            res = re.findall("^(\d+).*loopvideo_channel_id:"+str(self.channel_id), line.lstrip())#
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