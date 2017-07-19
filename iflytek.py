#!/usr/bin/env python
#coding:utf-8

import ctypes
from ctypes import *
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')
import log

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
class IflyTek:
    def __init__(self):
        self.__libmsc = ctypes.CDLL("./clibs/libmsc.so")
        self.__flag = True
        #answer/text
        self.__list1 = ['baike', 'calc', 'datetime', 'faq', 'openQA', 'chat']
        #text
        self.__list2 = ['weather']
        #
        self.__list3 = ['app', 'cookbook', 'flight', 'hotel', 'map', 'music', 'radio', 'restuarant', \
                        'schedule', 'stock', 'train', 'translation', 'tv', 'video', 'websearch', \
                        'website', 'weibo', 'flower', 'gift']
        #用户登录
        ret = self.__libmsc.MSPLogin(None, None, c_char_p("appid = appidtest"))
        if (0 != ret):
            #print ("MSPLogin failed , Error code %d"%(ret))
            log.debug("MSPLogin failed , Error code %d"%(ret))
            self.__flag = False

    def __del__(self):
        #退出登录 
        self.__flag = False
        self.__libmsc.MSPLogout()

    def __deal_data(self, data):
        jsondata = json.loads(data)
        if jsondata['rc'] != 0:
            return None
        else:
            if jsondata['service'] in self.__list1:
                return jsondata['answer']['text']
            elif jsondata['service'] in self.__list2:
                #weather
                if jsondata['semantic']['slots']['datetime']['date'] == "CURRENT_DAY":#今天
                    tmp_obj = jsondata['data']['result'][0]
                    res = "%s %s\n 天气：%s\n 气温：%s\n 风力：%s\n 来自:%s"%(tmp_obj['city'], tmp_obj['date'],\
                            tmp_obj['weather'], tmp_obj['tempRange'], tmp_obj['wind'], \
                            tmp_obj['sourceName'])
                    return res
                else:
                    for tmp_obj in jsondata['data']['result']:
                        if tmp_obj['date'] == jsondata['semantic']['slots']['datetime']['date']:
                            res = "%s %s\n 天气：%s\n 气温：%s\n 风力：%s\n 来自:%s"%(tmp_obj['city'], \
                                    tmp_obj['date'], tmp_obj['weather'], tmp_obj['tempRange'], \
                                    tmp_obj['wind'], tmp_obj['sourceName'])
                            return res
                    return None
            else:
                return None

    def sch_text(self, data):
        if(not self.__flag):
            return None 
        __msp_search = self.__libmsc.MSPSearch
        __msp_search.restype = c_char_p

        _data = create_string_buffer(data)
        _data_len = sizeof(_data)
        _len_point = pointer(c_uint(_data_len))
        _ret_p = pointer(c_int(0))

        rec_txt = __msp_search("nlp_version=2.0", _data, _len_point, _ret_p)
        if _ret_p.contents:
            #print ("MSPLogin failed , Error code %s"%(_ret_p.contents))
            log.warning("MSPLogin failed , Error code %s"%(_ret_p.contents))
            return None
        #print ("iflytek search api result: %s"%(rec_txt)) 
        log.debug("iflytek search api result: %s"%(rec_txt))
        return self.__deal_data(rec_txt)

if __name__ == '__main__':
    obj = IflyTek()
    res = obj.sch_text("南京大后天天气怎么样")
    print "\n\n"
    print res
