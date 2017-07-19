#!/usr/bin/env python #coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from db import DbProc


'''
#下面这个方法有问题，很奇怪？？？？？？
#方法1,实现__new__方法
#并在将一个类的实例绑定到类变量_instance上,
#如果cls._instance为None说明该类还没有实例化过,实例化该类,并返回
#如果cls._instance不为None,直接返回cls._instance
class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class DataCenter(Singleton):
'''


def singleton(cls, *args, **kw):
    '''
    for singleton base
    only add a row '@singleton' before the class define
    '''
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class DataCenter(object):
    """for date manager"""
    def __init__(self):
        self.__db = DbProc()
        self.__connected = 0
        self.__access_token = ''
        self.__jsapi_ticket = ''

    def connect_db(self, hostaddress, database_name, user, password):
        return self.__db.connect_db(hostaddress, database_name, user, password)

    def get_access_token(self):
        return self.__access_token

    def set_access_token(self, access_token):
        self.__access_token = access_token
        return self.__access_token

    def get_jsapi_ticket(self):
        return self.__jsapi_ticket

    def set_jsapi_ticket(self, jsapi_ticket):
        self.__jsapi_ticket = jsapi_ticket
        return self.__jsapi_ticket

    def add_user(self, openid, subscribe, nickname, sex, headimgurl, unionid):
        return self.__db.add_user(openid, subscribe, nickname, sex, headimgurl, unionid)

    def del_user_by_userid(self, userid):
        return self.__db.del_user_by_userid(userid)

    def del_user_by_openid(self, openid):
        return self.__db.del_user_by_openid(openid)
        '''
        data_list = self.__db.get_user_by_openid(openid)
        if len(data_list) == 0:
            return 0
        user_dict = data_list[0]
        print '000000000000000011111111111111'
        print user_dict
        if user_dict.has_key('id'):
            userid = user_dict['id']
            print userid
            return self.__db.del_user_by_userid(userid)
        else:
            print 'id is not found!!!!!!!!!'
            return -1
        '''

    def get_user(self, openid):
        return self.__db.get_user_by_openid(openid)

    # the follow is for table data
    def add_data(self, xdata):
        return self.__db.add_data(xdata)

    def del_data_by_id(self, id):
        return self.__db.del_data_by_id(id)

    def get_data_by_id(self, id):
        return self.__db.get_data_by_id(id)


    def search_data_by_title(self, titles, userid):
        return self.__db.search_data_by_title(titles, userid)

    def update_xdata(self, id, keys, values):
        return self.__db.update_xdata(id, keys, values)

    def get_not_read_id_from_xdata(self, userid):
        return self.__db.get_not_read_id_from_xdata(userid)

    def get_content_from_xdata(self, userid, id):
        return self.__db.get_content_from_xdata(userid, id)
