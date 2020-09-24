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
import myredis

md5 = hashlib.md5()
myrds = myredis.myRedis("./setting.conf")
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

#分析点播的m3u8的文件内容中的TS内容；
def parseM3u8_TS(str_m3u8):

    dict = {}
    i = 0
    while line in str_m3u8:
        if line.upper.find('.TS') > 0:
            dict[i] = line
            i = i + 1
    return dict
#查找TS内容中定位的位置；
def findTsSit(tsname, dict):
    
    for key in dict.keys():
        if dict[key].find(tsname) >= 0:
            return key

#保存当前的文件标识(MD5)进入到redis中,如果MD5相等，则返回真，如果MD5不等，则返回FALSE；
def isSamePrograme(url, channel):
    #此内容是为了在切换的过程中做一个比对；
    md5 = hashlib.md5()
    md5.update(url.encode("utf-8"))
    token = md5.hexdigest()
    global myrds

    token1 = myrds.getKey("loop_video_channel_"+str(channel))

    if token == token1:      
        return True
    else:
        myrds.setKey("loop_video_channel_"+str(channel), token)
        return False

def getTimeSequence(channel, url, last_mod):  #last_mod是传入的该频道的最后修改时间
    md5 = hashlib.md5()
    md5.update(last_mod.encode("utf-8"))
    lmod = md5.hexdigest()
    
    rlmod = myrds.getKey("loop_video_channel_"+str(channel)+"_mtime")
    rseq = myrds.getKey("loop_video_channel_"+str(channel)+"_seq")

    if rseq == None:
        rseq = 1
        myrds.setKey("loop_video_channel_"+str(channel)+"_seq", rseq)

    if lmod == rlmod:   #如果两个时间相同，则认为该m3u8内容没有更改；
        return int(rseq)
    else:
        seq = int(rseq) + 1
        myrds.setKey("loop_video_channel_"+str(channel)+"_seq", seq)
        return seq

#根据列表内空生成直播的M3u8内容，seq = timestamp, 如果sflag == True, 则认为是相同源，如果False则认为是不同源，需要增加补充信息，让编码器重新加载；
def mkLiveM3u8(dura_list, url_list, seq = 0, sflag=True):  #seq是新的序号，如果标志为true 则使用seq直接处理， 如果false, 则discountu
    nseq = seq
    str_head = ""
    str_seq = "" 
    du_str = ""

    #if not sflag:
    str_seq = "#EXT-X-DISCONTINUITY-SEQUENCE:0\n"  # 增加discountunity-sequence 对于不同的视频内容，需要重新的设定期sequence = 0
    du_str = "#EXT-X-DISCONTINUITY\n"

    #seq_arry = url_list[0].split("-")
    #i_seq = url_list[0].replace(".ts", "") 
    str_seq = str_seq+"#EXT-X-MEDIA-SEQUENCE:"+str(seq)+"\n"
    str_head = "#EXTM3U\n#EXT-X-VERSION:3\n"+str_seq
    str_m3u8 = ""
    max_sec = 0.000000

    for i in range(len(dura_list)):
        dura = "%.3f"%float(dura_list[i])
        str_m3u8 = str_m3u8 + "#EXTINF:"+dura+",\n"+url_list[i]+"\n"
        if max_sec < dura_list[i]:
            max_sec = dura_list[i]
    max_sec_i = int(max_sec + 0.5)
    #str_head = str_head + "#EXT-X-TARGETDURATION:"+str(max_sec_i)+"\n"+du_str
    str_head = str_head + "#EXT-X-TARGETDURATION:2\n"+du_str    
    return str_head+str_m3u8            

#杀死进程，根据pid杀死或根据cmd_str进行杀死；
def killProcess(cmd_str="", pid=0):
    

