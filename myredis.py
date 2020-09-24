# -*- coding: UTF-8 -*-
''' 
**********************************************************************************************
COPYRIGHT (C), Sunshine Cloud Video . Co., Ltd.  
File NAME:  myRedis.py
Author:  xiaobo      
Version: v1.0   
Date:  2020-09-16 
DESCRIPTION: Redis Class                          
Others: None
**********************************************************************************************          
'''

import redis    # 导入redis 模块
import configparser

class myRedis:

    host = None
    port = None
    pool = None

    def __init__(self, conf): 

        cf = configparser.ConfigParser()
        cf.read(conf)
        self.host = cf.get("redis", "host")
        self.port = cf.getint("redis", "port")
    
    def getConnect(self):
        
        if self.pool ==  None:
            self.pool = redis.ConnectionPool(host=self.host, port=self.port, decode_responses=True)              
        return redis.Redis(connection_pool=self.pool)
    
    def setKey(self, key, value, ipx = 1000*60*60*24):
        r = self.getConnect()
        if r == None:
            self.pool = None
            return None
        r.set(key, value, px=ipx)
        return "OK"
    def setKeyPx(self, key, value, ipx = 1000*60*60*24):
        r = self.getConnect()
        if r == None:
            self.pool = None
            return None
        r.set(key, value, px=ipx)
        return "OK"
    def getKey(self, key):
        r = self.getConnect()
        if r == None:
            self.pool = None
            return None
        return r.get(key)

    def delKey(self, key):
        r = self.getConnect()
        if r == None:
            self.pool = None
            return None
        return r.delete(key)

    def setHKey(self, hkey, hdict):
        r = self.getConnect()
        if r == None:
            self.pool = None
            return None
        return r.hmset(hkey, hdict)

    def getHKey(self, hkey):
        r = self.getConnect()
        if r == None:
            self.pool = None
            return None
        return r.hgetall(hkey)
        