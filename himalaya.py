#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import hmac
import hashlib

import time

import json
import urllib
import urllib2

import sys
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
class Himalaya:
    def __init__(self):
        self.__timeout = 60
        self.__app_key = "appkey"
        self.__device_id = "deviceid"
        self.__app_secret = "appsecret"
        self.__access_token_url = "http://api.ximalaya.com/oauth2/secure_access_token"
        self.__url = "http://api.ximalaya.com"
        self.__category_url = "/categories/human_recommend"
        self.__tag_url = "/tags/list"
        self.__track_url = "/tracks/hot"
        self.__album_url = "/albums/list"
        self.__search_album_url = "/search/albums"
        self.__search_track_url = "/search/tracks"
        self.__album_browse_url = "/albums/browse"
        self.get_access_token()

    def http_get(self, url):
        try:
            resp = urllib2.urlopen(url.encode('utf-8'), timeout = self.__timeout).read()
            return json.loads(resp)
        except Exception, Argument:
            log.error(Argument)
            return None

    def http_post(self, url, data, header_type):
        header = {'Content-Type': header_type}
        try:
            request = urllib2.Request(url=url, headers=header, data=data)
            resp = urllib2.urlopen(request, timeout=self.__timeout).read()
            return json.loads(resp)
        except Exception, Argument:
            log.error(Argument)
            return None


    def __common_params(self, params, os_type, pack_id):
        # common params
        params['app_key'] = self.__app_key
        params['device_id'] = self.__device_id
        params['client_os_type'] = os_type
        if pack_id is not None:
            params['pack_id'] = pack_id
        params['access_token'] = self.__access_token

    def __set_recommendation(self, track):
        tmp_dict = {}
        tmp_dict['id'] = track['id']
        tmp_dict['title'] = track['track_title']
        tmp_dict['author'] = track['announcer']['nickname']
        if track['source'] == 1:
            tmp_dict['source'] = '用户原创'
        else:
            tmp_dict['source'] = '用户转采'
        tmp_dict['intro'] = track['track_intro']
        tmp_dict['duration'] = track['duration']
        tmp_dict['play_url'] = track['play_url_32']
        tmp_dict['download_url'] = track['download_url']
        tmp_dict['download_size'] = track['download_size']
        return tmp_dict

    #argv is a dict about key-value, return sig and params list
    def __sig_calc(self, argv):
        if not argv:
            return None
        #sort argv by keys and join
        tmp_list = sorted(argv.keys())
        argv_list = []
        for item in tmp_list:
            tmp_str = "&%s=%s"%(item, argv[item])
            argv_list.append(tmp_str)
        tmp_res = (''.join(argv_list))[1:]

        #calc sign
        ##base64 encode
        b64_res = base64.b64encode(tmp_res)
        ##hmac-sha1 encry
        h_s_res = hmac.new(self.__app_secret, b64_res, hashlib.sha1).digest()
        ##md5
        tmp_hash = hashlib.md5()
        tmp_hash.update(h_s_res)
        res = tmp_hash.hexdigest()
        #tmp_param = tmp_res + "&sig=%s"%(res)
        argv['sig'] = res
        tmp_param = urllib.urlencode(argv)
        return [res, tmp_param]

    def get_access_token(self):
        params = {}
        params['client_id'] = self.__app_key
        params['grant_type'] = "client_credentials"
        params['device_id']= self.__device_id
        params['timestamp'] = long(time.time() * 1000)
        tmp_num = float(str(params['timestamp'])[8:])
        params['nonce'] = str(tmp_num * tmp_num)
        data = self.__sig_calc(params)

        body = data[1]
        tmp_url = self.__access_token_url
        """
        resp = urllib.urlopen(tmp_url, body).read()
        res = json.loads(resp)
        """
        res = self.http_post(tmp_url, body, 'application/x-www-form-urlencoded')
        if res is None:
            return
        #print ("==>>> get_access_token_resp:%s"%(res))
        log.debug("get_access_token response:%s"%(res))
        if not res.has_key('error_no'):
            self.__access_token = res['access_token']
            self.__expires_in = res['expires_in']
        else:
            self.__access_token = ''
            self.__expires_in = 0

    def categories_human_recommend(self, os_type, pack_id):
        params = {}
        self.__common_params(params, os_type, pack_id)
        data = self.__sig_calc(params)
        tmp_url = "%s%s?%s"%(self.__url, self.__category_url, data[1])
        return self.http_get(tmp_url)

    def tags_list(self, os_type, pack_id, tag_type, category_id):
        params = {}
        self.__common_params(params, os_type, pack_id)
        params['category_id'] = category_id
        params['type'] = tag_type
        data = self.__sig_calc(params)
        tmp_url = "%s%s?%s"%(self.__url, self.__tag_url, data[1])
        return self.http_get(tmp_url)

    def tracks_hot(self, os_type, pack_id, category_id, tag_name):
        params = {}
        self.__common_params(params, os_type, pack_id)
        params['category_id'] = category_id
        params['tag_name'] = tag_name
        data = self.__sig_calc(params)
        tmp_url = "%s%s?%s"%(self.__url, self.__track_url, data[1])
        return self.http_get(tmp_url)

    def albums_list(self, os_type, pack_id, category_id, tag_name, dimension):
        params = {}
        self.__common_params(params, os_type, pack_id)
        params['category_id'] = category_id
        params['tag_name'] = tag_name
        params['calc_dimension'] = dimension
        data = self.__sig_calc(params)
        tmp_url = "%s%s?%s"%(self.__url, self.__album_url, data[1])
        return self.http_get(tmp_url)

    def search_albums(self, os_type, pack_id, param, category_id = None):
        params = {}
        self.__common_params(params, os_type, pack_id)
        params['q'] = param
        data = self.__sig_calc(params)
        tmp_url = "%s%s?%s"%(self.__url, self.__search_album_url, data[1])
        return self.http_get(tmp_url)

    def search_tracks(self, os_type, pack_id, param, category_id = None):
        params = {}
        self.__common_params(params, os_type, pack_id)
        params['q'] = param
        data = self.__sig_calc(params)
        tmp_url = "%s%s?%s"%(self.__url, self.__search_track_url, data[1])
        return self.http_get(tmp_url)

    def album_browse(self, os_type, pack_id, album_id, count = 20, sort = "asc", page = 1):
        if count > 200:
            count = 200
        params = {}
        self.__common_params(params, os_type, pack_id)
        params['album_id'] = album_id
        params['sort'] = sort
        params['page'] = page
        params['count'] = count
        data = self.__sig_calc(params)
        tmp_url = "%s%s?%s"%(self.__url, self.__album_browse_url, data[1])
        return self.http_get(tmp_url)

    def get_recommendation_tmp(self, os_type, pack_id):
        recommendation = {'code': 0}
        #获取热门分类
        res = self.categories_human_recommend(os_type, pack_id)
        for item in res:
            #print "===>> category:", item['category_name'].encode("utf-8"), item['id']
            if item['id'] != 8:
                continue
            category_id = item['id']
            category_name = item['category_name']
            print "====>>>> categor name, id:", category_name, category_id
            #log.info("category_name:%s, category_id:%d"%(category_name, category_id))

            #获取专辑tag
            res = self.tags_list(os_type, pack_id, 0, category_id)
            tag_names = []
            for item in res:
                tag_names.append(item['tag_name'])

            # category + tag 获取声音
            recommendation['recommendation'] = []
            recommendation['code'] = 0
            cnt = 0
            for item in tag_names:
                """
                if cmp(item, u"干货铺子"):
                    #print "===>>> tag_name:", item.encode('utf-8')
                    print "===>>> tag_name:", item
                    continue
                """
                print "===>>> tag_name:", item
                res = self.albums_list(os_type, pack_id, category_id, item, 3)
                if res.has_key('albums'):
                    tmp_list = res['albums']
                    for track in tmp_list:
                        print "==>>>album: ", track['album_title']
                else:
                    pass
        else:
            recommendation = {'code': 0}
            recommendation['error'] = 'no data'

        return json.dumps(recommendation, ensure_ascii = False).encode('utf-8')

    def get_recommendation(self, os_type, pack_id, query_param = ''):
        recommendation = {'code': 0}

        if "luogic_show" in query_param:
            return self.get_sound_by_album_id(os_type, pack_id, 239463, 1)
        else:
            #"""
            res = self.tracks_hot(os_type, pack_id, 18, "科学迷")
            #res = self.tracks_hot(os_type, pack_id, 1, "头条")
            if (res is not None) and res.has_key('tracks'):
                recommendation['recommendation'] = []
                tmp_list = res['tracks']
                for track in tmp_list:
                    recommendation['recommendation'].append(self.__set_recommendation(track))
            else:
                recommendation['code'] = -1
                recommendation['error'] = 'no data'
            return json.dumps(recommendation, ensure_ascii = False).encode('utf-8')
            #"""
            #return self.find_track(os_type, pack_id, "学点 知识")


    def get_sound_by_album_id(self, os_type, pack_id, id, count = 20, sort = "asc", page = 1):
        recommendation = {'code': 0}
        res = self.album_browse(os_type, pack_id, id, count, sort, page)
        if (res is not None) and res.has_key('tracks'):
            recommendation['recommendation'] = []
            track_list = res['tracks']
            for track in track_list:
                recommendation['recommendation'].append(self.__set_recommendation(track))
        else:
            recommendation = {'code': -1}
            recommendation['error'] = 'no data'
        #log.debug(json.dumps(recommendation, ensure_ascii = False).encode('utf-8'))
        print json.dumps(recommendation, ensure_ascii = False).encode('utf-8')
        return json.dumps(recommendation, ensure_ascii = False).encode('utf-8')

    def find_album(self, os_type, pack_id, param):
        res = self.search_albums(os_type, pack_id, param)
        for item in res['albums']:
            print item['album_title'], item['id']
    
    def find_track(self, os_type, pack_id, param):
        recommendation = {'code': 0}
        res = self.search_tracks(os_type, pack_id, param)
        if (res is not None) and res.has_key('tracks'):
            recommendation['recommendation'] = []
            for track in res['tracks']:
                recommendation['recommendation'].append(self.__set_recommendation(track))
        else:
            recommendation = {'code': -1}
            recommendation['error'] = 'no data'
        return json.dumps(recommendation, ensure_ascii = False).encode('utf-8')
    
if __name__ == '__main__':
    obj = Himalaya()
    #resp = obj.get_recommendation(4, None, "luogic_show")
    #resp = obj.find_album(4, None, "罗辑思维")
    resp = obj.find_album(4, None, "罗振宇")
    #resp = obj.get_recommendation_tmp(4, None)
    #obj.find_album(4, None, "科普")
    #obj.find_track(4, None, "科技 创新")
    #obj.get_sound_by_album_id(4, None, 239463)

