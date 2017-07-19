#!/usr/bin/env python
#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('../')
import log

import urllib2
import json


class LingWeather(object):
    """for ling weather
    http://101.201.72.216:8082/jibo/question
    {
        'data':{
            'attributes': {
                'emotion': '0',
                'nlu': {
                    u'intention': u'weather', u'time_normalized': {u'M': 0, u'd': 20, u'H': 0, u'm': 4, u'S': 0, u'y': 2017}, u'place': u'\u5317\u4eac', u'time': u'\u4eca\u5929'}}}

    {
        "data": {
            "type": "weather",
            "attributes": {
                "userid": "jibo",
                "words": "今天多少度",
                "emotion": "0",
                "score": 0,
                "nlu": {
                    "answer": "抱歉, 天气信息查询不到，意图为weather",
                    "domain": "weather",
                    "code": 0,
                    "related": -1,
                    "param": {
                        "intention": "weather",
                        "time_normalized": {
                            "d": 19,
                            "H": 0,
                            "M": 0,
                            "m": 4,
                            "S": 0,
                            "y": 2017
                        },
                        "place": "北京",
                        "time": "今天"
                    }
                }
            }
        }
    }

    {
      "data": {
        "type": "answer",
        "id": "none",
        "attributes": {
          "domain": "weather",
          "data": {
            "answer": "今天北京多云,温度为14摄氏度。",
            "animation": "",
            "tip": "要少穿衣服哦!",
            "tip_type": "温度高",
            "time": "今天",
            "place": "北京",
            "desc": "多云",
            "date": "2017-4-19",
            "temp": "14",
            "score": 8
          }
        }
      }
    }

    """
    def __init__(self):
        self.__url = 'http://101.201.72.216:8082/jibo/question'
        self.__session_key = ''

    #### access token operation ####
    def search_weather(self, param, userid):
        data = {
            "data":{
                "type":"weather",
                "attributes":{
                    "userid":userid,
                    "words":"今天多少度",
                    "emotion":"0",
                    "score":0,
                    "nlu":{
                        "answer": "抱歉, 天气信息查询不到，意图为weather",
                        "domain": "weather",
                        "code": 0,
                        "related": -1,
                        "param": {
                            "intention": "weather",
                            "time_normalized": {
                              "d": 19,
                              "H": 0,
                              "M": 0,
                              "m": 4,
                              "S": 0,
                              "y": 2017
                            },
                            "place": "北京",
                            "time": "今天"
                        }
                    }
                }
            }
        }
        data['data']['attributes']['nlu'] = param
        #print data
        log.info(data)
        headers = {'Content-Type': 'application/json'}
        request = urllib2.Request(url=self.__url, headers=headers, data=json.dumps(data))
        urlResp = urllib2.urlopen(request)

        urlResp = urlResp.read()
        urlResp = json.loads(urlResp)
        #print '=========================================='
        #print urlResp
        log.debug('==========================================')
        log.debug(urlResp)
        return urlResp







