# -*- coding: UTF-8 -*-
''' 
**********************************************************************************************
COPYRIGHT (C), Sunshine Cloud Video . Co., Ltd.  
File NAME:  myExc.py
Author:  xiaobo      
Version: v1.0   
Date:  2020-09-16 
DESCRIPTION: Mysql Class                          
Others: None
**********************************************************************************************          
'''
import pymysql
from dbutils.pooled_db import PooledDB
import json
import myglobal as mygl

pool = None
class myExc:

    db_host = None
    db_port = None
    db_user = None
    db_pass = None
    db_pool = None
    db_database = None    
    conn = None

    #初始化过程中需要指定读取配置文件的名称；
    def __init__(self):

        self.db_host = mygl.get_my("db_host")
        self.db_port = mygl.get_my("db_port")
        self.db_user = mygl.get_my("db_user")
        self.db_pass = mygl.get_my("db_pass") 
        self.db_pool = mygl.get_my("db_pool")
        self.db_database = mygl.get_my("db_database")        
        global pool
        if not pool:
            #建立连接池，共建立10个连接，可以提高效度，节省资源的消耗；
            pool = PooledDB(pymysql, int(self.db_pool) ,host=self.db_host, user=self.db_user, passwd=self.db_pass,db=self.db_database ,port=int(self.db_port), charset="utf8", autocommit=True) #5为连接池里的最少连接数
        #self.conn = pymysql.connect(host=self.db_host, port= int(self.db_port), user=self.db_user, password=self.db_pass, database=self.db_database, charset="utf8", autocommit=True)
        self.conn = pool.connection()
    #查询数据库，返回json列表；
    def queryToJson(self, sql):

        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = self.sql_fetch_json(cursor)
        cursor.close()
        return result

    #该函数把结果转成json的格式；
    def sql_fetch_json(self, cursor: pymysql.cursors.Cursor):

        keys = []
        for column in cursor.description:
            keys.append(column[0])
        key_number = len(keys)

        json_data = []
        for row in cursor.fetchall():
            item = dict()
            for q in range(key_number):
                item[keys[q]] = row[q]
            json_data.append(item)

        return json_data