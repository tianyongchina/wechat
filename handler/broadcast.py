#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import hashlib
import reply
import json
import thread
import tornado.gen
import tornado.escape
import tornado.httpclient
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from dataproc.datacenter import DataCenter
from music.baidu import BaiduMusicSearch
from weather.lingweather import LingWeather
from time import strftime,gmtime
from datetime import datetime
from himalaya import Himalaya

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("..")
import log

lingx_split_str = "@&@"

class CollectionHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(4)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self, funcname): 
        body = json.loads(self.request.body)
        yield self.run_sql_proc(body, funcname)

    @run_on_executor
    def run_sql_proc(self, body, funcname):
        try:
            content = {'code': 0}
            if funcname == 'notread':
                if(body.has_key('userid')):
                    userid = body['userid']
                    res_list = DataCenter().get_not_read_id_from_xdata(userid)
                    list_dict = []
                    for i in range(len(res_list)):
                        tmp = {}
                        tmp['id'] = res_list[i]['id']
                        list_dict.append(tmp)
                    content['collections'] = list_dict
                else:
                    content['code'] = -1
                    content['error'] = 'userid is needed.'
            elif funcname == 'content':
                if (body.has_key('userid') and body.has_key('id')):
                    userid = body['userid']
                    id = body['id']
                    res_list = DataCenter().get_content_from_xdata(userid, id)
                    content['id'] = res_list[0]['id']
                    content['title'] = res_list[0]['title']
                    content['author'] = res_list[0]['author']
                    content['source'] = res_list[0]['datasource']
                    content['subject'] = res_list[0]['aidata'].split(lingx_split_str)
                    content['original'] = res_list[0]['originaldata'].split(lingx_split_str)

                    #修改accesstime
                    #DataCenter().update_xdata(id, 'accesstime', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                else:
                    content['code'] = -1
                    content['error'] = 'userid and id are needed.'
            elif funcname == 'status':
                if (body.has_key('article_list')):
                    for item in body['article_list']:
                        #修改accesstime
                        DataCenter().update_xdata(item['id'], 'accesstime', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    content['code'] = -1
                    content['error'] = 'article_list is empty.'
            else:
                pass
            #print content
            log.debug(content)
            self.write(tornado.escape.json_encode(content))
            self.finish()
        except Exception, Argument:
            log.error(Argument)
            self.finish(Argument)

class RecommendHandler(tornado.web.RequestHandler):

    executor = ThreadPoolExecutor(4)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        body = json.loads(self.request.body)
        yield self.run_proc(body)

    @run_on_executor
    def run_proc(self, body):
        try:
            if body.has_key('client_os_type'):
                pack_id = None
                query_param = ''
                if body.has_key('pack_id'):
                    pack_id = body['pack_id']
                if body.has_key('query_param'):
                    query_param = body['query_param']
                resp = Himalaya().get_recommendation(body['client_os_type'], pack_id, query_param)
                self.finish(resp)
            else:
                tmp_dict = {'code': -1, "error": "need clent os type param"}
                self.finish(json.dumps(tmp_dict))

        except Exception, Argument:
            log.error(Argument)
            self.finish(Argument)

class SongHandler(tornado.web.RequestHandler):
    #url: /song/info
    def post(self):
        body = json.loads(self.request.body)
        response = {'code': 0}
        if body.has_key('songId'):
            search_result = BaiduMusicSearch().search_song_byid(body['songId'])
            response['searchResult'] = search_result
        else:
            response['code'] = -1
            response['error'] = "not found song id."
        json_data = json.dumps(response, ensure_ascii=False)
        log.info(json_data)
        self.write(json_data)
