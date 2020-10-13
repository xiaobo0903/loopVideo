# -*- coding: UTF-8 -*-
''' 
**********************************************************************************************
COPYRIGHT (C), Sunshine Cloud Video . Co., Ltd.  
File NAME:  pnacos.py
Author:  xiaobo      
Version: v1.0   
Date:  2020-09-16 
DESCRIPTION: Mysql Class                          
Others: None
**********************************************************************************************          
'''
import nacos
import socket
import time
import log as mylog
import threading

class pnacos:

    SERVER_ADDRESSES = "10.10.10.100"
    NAMESPACE = ""
    SERVICENAME = ""
    port = 0
    client = None
    ip = None

    def __init__(self, nacos_ip, namespace, servicename):

        self.SERVER_ADDRESSES = nacos_ip
        self.SERVICENAME = servicename
        self.NAMESPACE = namespace
        
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(('114.114.114.114',80))
            self.ip=s.getsockname()[0]
        finally:
            s.close()
        mylog.logger.info("the machine IP is :"+self.ip)
        self.client = nacos.NacosClient(self.SERVER_ADDRESSES, namespace=self.NAMESPACE)
    
    #注册Nacos实例
    def RegInstance(self):
        self.client.add_naming_instance(self.SERVICENAME, self.ip, self.port, "", 1.0, "", True, True)
        #curl -X POST 'http://127.0.0.1:8848/nacos/v1/ns/instance?port=8848&healthy=true&ip=11.11.11.11&weight=1.0&serviceName=nacos.test.3&encoding=GBK&namespaceId=n1''

    #查询Nacos中实例的详情
    def QueryInstance(self):
        i_states = self.client.get_naming_instance(self.SERVICENAME, self.ip, self.port, "")
        #mylog.logger.info(i_states)

    #发送实例的心跳
    def SendHeartBeat(self):
        while True:
            i_beat = self.client.send_heartbeat(self.SERVICENAME, self.ip, self.port,  "", 1.0, "{}")
            #mylog.logger.info(i_beat) 
            time.sleep(5)
    #启动nacos的注册运行
    def start(self):
        self.RegInstance()
        time.sleep(5)
        self.QueryInstance()
        #启动心跳线程；
        t = threading.Thread(target=self.SendHeartBeat)
        t.start()

if __name__ == '__main__':

    pn = pnacos()
    pn.start()
    while True:
        time.sleep(10)


