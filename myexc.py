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
 
import configparser
import pymysql
import json
import myglobal as mygl

class myExc:

    db_host = None
    db_port = None
    db_user = None
    db_pass = None
    db_database = None
    conn = None

    #初始化过程中需要指定读取配置文件的名称；
    def __init__(self):

        self.db_host = mygl.get_my("db_host")
        self.db_port = mygl.get_my("db_port")
        self.db_user = mygl.get_my("db_user")
        self.db_pass = mygl.get_my("db_pass") 
        self.db_database = mygl.get_my("db_database")
        self.conn = pymysql.connect(host=self.db_host, port= int(self.db_port), user=self.db_user, password=self.db_pass, database=self.db_database, charset="utf8", autocommit=True)
    
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

