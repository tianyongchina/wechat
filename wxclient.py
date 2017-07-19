# -*- coding: utf-8 -*-
# filename: wxclient.py

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
import json
from dataproc.datacenter import DataCenter
import log



class WeixinClient:
    '''the client is used to send message to weixin platform and get information'''
    def __init__(self):
        self.__data_global_obj = DataCenter()
        self.__accessToken = self.__data_global_obj.get_access_token()
        self.__jsapi_ticket = self.__data_global_obj.get_jsapi_ticket()

    def _decode_list(data):
        rv = []
        for item in data:
            if isinstance(item, unicode):
                item = item.encode('utf-8')
            elif isinstance(item, list):
                item = _decode_list(item)
            elif isinstance(item, dict):
                item = _decode_dict(item)
            rv.append(item)
        return rv

    def _decode_dict(data):
        rv = {}
        for key, value in data.iteritems():
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            elif isinstance(value, list):
                value = _decode_list(value)
            elif isinstance(value, dict):
                value = _decode_dict(value)
            rv[key] = value
        return rv

    #### access token operation ####
    def get_access_token(self):
        appId = "appId"
        appSecret = "appSecret"

        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
               "client_credential&appid=%s&secret=%s" % (appId, appSecret))
        urlResp = urllib.urlopen(postUrl)
        urlResp = json.loads(urlResp.read())

        if urlResp.has_key('access_token'):
            self.__accessToken = urlResp['access_token']
            self.__leftTime = urlResp['expires_in']

            #get jsapi_ticket
            postUrl = ("https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi" % (self.__accessToken))
            urlResp = urllib.urlopen(postUrl)
            urlResp = json.loads(urlResp.read())

            if urlResp.has_key('ticket') and urlResp['errcode']==0:
                self.__jsapi_ticket = urlResp['ticket']

            # restore in datacenter
            self.__data_global_obj.set_access_token(self.__accessToken)
            self.__data_global_obj.set_jsapi_ticket(self.__jsapi_ticket)

        #print "access_token: %s" % self.__accessToken
        #print "saved access_token: %s" % DataCenter().get_access_token()
        #print "expires_in: %s" % self.__leftTime
        log.info("access_token: %s"%(self.__accessToken))
        log.info("saved access_token: %s"%(DataCenter().get_access_token()))
        log.info("expires_in: %s"%(self.__leftTime))

    def check_access_token(self):
        if len(self.__accessToken) == 0:
            get_access_token()

    #### menu operation ####
    def create_menu(self, postData):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % self.__data_global_obj.get_access_token()
        if isinstance(postData, unicode):
            postData = postData.encode('utf-8')
        urlResp = urllib.urlopen(url=postUrl, data=postData)
        #print urlResp.read()
        log.info(urlResp.read())

    def query_menu(self):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % self.__data_global_obj.get_access_token()
        urlResp = urllib.urlopen(url=postUrl)
        #print urlResp.read()
        log.info(urlResp.read())


    def delete_menu(self):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % self.__data_global_obj.get_access_token()
        urlResp = urllib.urlopen(url=postUrl)
        #print urlResp.read()
        log.info(urlResp.read())

    #获取自定义菜单配置接口
    def get_current_selfmenu_info(self):
        postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % self.__data_global_obj.get_access_token()
        urlResp = urllib.urlopen(url=postUrl)
        #print urlResp.read()
        log.info(urlResp.read())

    #### user operation ####
    def get_user_info(self, openid):
        postUrl = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN " \
                  % (self.__data_global_obj.get_access_token(), openid)
        urlResp = urllib.urlopen(postUrl)
        recJson = urlResp.read()    #read智能执行一次，之后就没有值了
        #print recJson
        log.info(recJson)
        urlResp = json.loads(recJson)
        #return _decode_dict(urlResp)
        return urlResp






if __name__ == '__main__':
    myMenu = Menu()
    postJson = """
    {
        "button":
        [
            {
                "type": "click",
                "name": "开发指引",
                "key":  "mpGuide"
            },
            {
                "name": "公众平台",
                "sub_button":
                [
                    {
                        "type": "view",
                        "name": "更新公告",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                    },
                    {
                        "type": "view",
                        "name": "接口权限说明",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                    },
                    {
                        "type": "view",
                        "name": "返回码说明",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433747234&token=&lang=zh_CN"
                    }
                ]
            }
          ]
    }
    """
    accessToken = GetAccessToken().get_access_token()
    myMenu.delete(accessToken)
    #myMenu.create(postJson, accessToken)
