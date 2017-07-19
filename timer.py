# -*- coding: utf-8 -*-
# filename: timer.py
import urllib
import time
import json
import log

class GetAccessToken:
    def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0
    def real_get_access_token(self):
        appId = "appId"
        appSecret = "appSecret"

        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
               "client_credential&appid=%s&secret=%s" % (appId, appSecret))
        urlResp = urllib.urlopen(postUrl)
        urlResp = json.loads(urlResp.read())

        self.__accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']
        #print "access_token: %s" % self.__accessToken
        #print "expires_in: %s" % self.__leftTime
        log.info("access_token: %s"%(self.__accessToken))
        log.info("expires_in: %s"%(self.__leftTime))
        


    def get_access_token(self):
        if self.__leftTime < 10:
            self.real_get_access_token()
        return self.__accessToken

    def run(self):
        while(True):
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                self.__real_get_access_token()


