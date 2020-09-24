# -*- coding: utf-8 -*- 
import configparser

def _init():#初始化
    global _global_dict
    _global_dict = {}  
 
 
def set_value(key,value):
    """ 定义一个全局变量 """
    _global_dict[key] = value

def get_value(key,defValue=None):
    try:
        return _global_dict[key]
    except KeyError:
        return defValue

def get_dict():
    return _global_dict

def set_dict(dict):
    _global_dict = dict

def _myinit(conf):#mysql配置文件初始化
    
    global _global_my
    _global_my = {}    
    cf = configparser.ConfigParser()
    cf.read(conf)
    _global_my["db_host"] = cf.get("mysqldb", "db_host")
    _global_my["db_port"] = cf.getint("mysqldb", "db_port")
    _global_my["db_user"] = cf.get("mysqldb", "db_user")
    _global_my["db_pass"] = cf.get("mysqldb", "db_pass") 
    _global_my["db_database"] = cf.get("mysqldb", "db_database")

def get_my(key,defValue=None):
    try:
        return _global_my[key]
    except KeyError:
        return defValue