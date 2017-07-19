#!/usr/bin/env python
#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
import log

import urllib
import json
import random


song_page_size = 10

def DebugPrint(msg):
    log.debug(msg)
    #print msg

class BaiduAuth(object):
    def __init__(self):
        self.__access_token = ''
        self.__session_key = ''

    #### access token operation ####
    def get_access_token(self):

        grant_type = 'client_credentials'
        client_id = ''
        client_secret = ''
        #scope  = '301 302 303 304 305 306 307'
        #scope = 'music_media_basic music_musicdata_basic music_userdata_basic music_search_basic music_media_premium music_audio_premium music_audio_hq'

        postUrl = ("https://openapi.baidu.com/oauth/2.0/token?"
                    "grant_type=%s&client_id=%s&client_secret=%s" %
                   (grant_type, client_id, client_secret))

        postUrl = urllib.quote(postUrl) #URL关键字转义
        urlResp = urllib.urlopen(postUrl)
        urlResp = urlResp.read()
        #print urlResp
        urlResp = json.loads(urlResp)
        #print urlResp
        DebugPrint(urlResp)

        if urlResp.has_key('access_token'):
            self.__accessToken = urlResp['access_token']
            self.__session_key = urlResp['session_key']

        #print "baidu music access_token: %s" % self.__accessToken
        #print "baidu music session_key: %s" % self.__session_key
        log.info("baidu music access_token: %s" % self.__accessToken)
        log.info("baidu music session_key: %s" % self.__session_key)


class BaiduMusicSearch(object):
    """
    access_token: 通过百度合作方式取得
    """
    def __init__(self):
        self.__access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        self.__session_key = ''

    #### search song ####
    def search_song_byid(self, songid):
        postUrl = ("https://openapi.baidu.com/rest/2.0/music/song/info?access_token=%s&songid=%s" %
                   (self.__access_token, songid))

        urlResp = urllib.urlopen(postUrl)
        urlResp = urlResp.read()
        urlResp = json.loads(urlResp)
        #print urlResp
        DebugPrint(urlResp)

        search_result = {}
        if urlResp.has_key('songurl') and urlResp['songurl'].has_key('url') and urlResp.has_key('songinfo'):
            tmp_list = urlResp['songurl']['url']
            content = urlResp['songinfo']['content']
            if len(tmp_list) > 0:
                search_result['key'] = ''
                search_result['style'] = ''
                search_result['fromLocal'] = False
                search_result['url'] = tmp_list[0]['file_link']
                search_result['duration'] = tmp_list[0]['file_duration']
                search_result['title'] = content['title']
                search_result['artist'] = content['author']
                search_result['songId'] = content['song_id']
                search_result['pic'] = content['pic_s500']
                testextern = {}
                testextern['ui'] = ''  #UI方案
                testextern['tts'] = '现在播放' + search_result['artist'] + '的' + search_result['title']
                search_result['test'] = testextern
                #return json.dumps(search_result).encode('utf-8')

        return search_result

    #### common search ####
    def search_common(self, query):
        postUrl = ("http://tingapi.ting.baidu.com/v1/restserver/ting?from=qianqian&version=2.1&method=baidu.ting.search.catalogSug&format=json&query=%s" %
                   (query))
        '''
        {
            "song": [
                {
                    "bitrate_fee": "{\"0\":\"129|-1\",\"1\":\"-1|-1\"}",
                    "weight": "26810",
                    "songname": "菊花台",
                    "songid": "252832",
                    "has_mv": "0",
                    "yyr_artist": "0",
                    "artistname": "周杰伦",
                    "resource_type_ext": "0",
                    "resource_provider": "1",
                    "control": "0000000000",
                    "encrypted_songid": "85053dba00958414d0dL"
                },
                {
                    "bitrate_fee": "{\"0\":\"129|-1\",\"1\":\"-1|-1\"}",
                    "weight": "420",
                    "songname": "菊花台(钢琴演奏版)",
                    "songid": "736044",
                    "has_mv": "0",
                    "yyr_artist": "0",
                    "artistname": "周杰伦",
                    "resource_type_ext": "0",
                    "resource_provider": "1",
                    "control": "0000000000",
                    "encrypted_songid": "7805b3b2c0958414d15L"
                }
            ],
            "error_code": 22000,
            "order": "song"
        }
'''
        #print postUrl
        DebugPrint(postUrl)
        #postUrl = urllib.quote(postUrl) #URL关键字转义
        urlResp = urllib.urlopen(postUrl)
        urlResp = urlResp.read()
        urlResp = json.loads(urlResp)
        #print urlResp
        DebugPrint(urlResp)

        #parse
        search_result = {}
        if urlResp.has_key('song'):
            tmp_list = urlResp['song']
            if len(tmp_list) > 0:
                #取出第一个
                song_index = 0
                songid = tmp_list[song_index]['songid']
                search_result = self.search_song_byid(songid)

                #寻找作者其他歌曲
                song_list = self.search_list(tmp_list[song_index]['artistname'].encode('utf-8'), songid)
                search_result['list'] = song_list

        DebugPrint(search_result)
        return search_result


    #### list search ####
    def search_list(self, query, not_song_id):
        postUrl = ("http://tingapi.ting.baidu.com/v1/restserver/ting?from=qianqian&version=2.1&method=baidu.ting.search.catalogSug&format=json&query=%s" %
                   (query))
        '''
        {
            "song": [
                {
                    "bitrate_fee": "{\"0\":\"129|-1\",\"1\":\"-1|-1\"}",
                    "weight": "477610",
                    "songname": "告白气球",
                    "songid": "266322598",
                    "has_mv": "0",
                    "yyr_artist": "0",
                    "resource_type_ext": "0",
                    "artistname": "周杰伦",
                    "info": "",
                    "resource_provider": "1",
                    "control": "0000000000",
                    "encrypted_songid": "2507fdfc2a60958414cceL"
                },
                {
                    "bitrate_fee": "{\"0\":\"129|-1\",\"1\":\"-1|-1\"}",
                    "weight": "67740",
                    "songname": "青花瓷",
                    "songid": "354387",
                    "has_mv": "0",
                    "yyr_artist": "0",
                    "resource_type_ext": "0",
                    "artistname": "周杰伦",
                    "info": "",
                    "resource_provider": "1",
                    "control": "0000000000",
                    "encrypted_songid": "6605568530958414d10L"
                }
            ],
            "album": [
                {
                    "albumname": "周杰伦的床边故事",
                    "weight": "556840",
                    "artistname": "周杰伦",
                    "resource_type_ext": "0",
                    "artistpic": "http://qukufile2.qianqian.com/data2/pic/ed58ab93ec08650f765bc40500ba47b1/273945524/273945524.jpg@s_0,w_40",
                    "albumid": "266322553"
                }
            ],
            "order": "artist,song,album",
            "error_code": 22000,
            "artist": [
                {
                    "yyr_artist": "0",
                    "artistname": "周杰伦",
                    "artistid": "7994",
                    "artistpic": "http://qukufile2.qianqian.com/data2/pic/046d17bfa056e736d873ec4f891e338f/540336142/540336142.jpg@s_0,w_48",
                    "weight": "709240"
                }
            ]
        }

        "list": [
            {
                "fromLocal": false,
                "songId": "257535276",
                "tts": ""
            },
            {
                "fromLocal": false,
                "songId": "1999341",
                "tts": ""
            }
        ]
'''
        #print postUrl
        DebugPrint(postUrl)
        #postUrl = urllib.quote(postUrl) #URL关键字转义
        urlResp = urllib.urlopen(postUrl)
        urlResp = urlResp.read()
        urlResp = json.loads(urlResp)
        #print urlResp
        DebugPrint(urlResp)

        #parse
        song_list = []
        if urlResp.has_key('song'):
            tmp_list = urlResp['song']
            for song_tmp in tmp_list:
                if song_tmp['songid'] != not_song_id:       #去掉刚才选择的歌曲
                    song_info = {}
                    song_info['fromLocal'] = False
                    song_info['songId'] = song_tmp['songid']
                    song_info['tts'] = ''
                    song_list.append(song_info)
            #search_result['list'] = song_list

        DebugPrint(song_list)
        return song_list


    #### search style tag ####
    def search_by_style(self, style):
        postUrl = ("https://openapi.baidu.com/rest/2.0/music/tag/songlist?access_token=%s&tagname=%s&page_size=%d&page_no=1" %
                   (self.__access_token, style, song_page_size))

        urlResp = urllib.urlopen(postUrl)
        urlResp = urlResp.read()
        urlResp = json.loads(urlResp)
        #print urlResp
        DebugPrint(urlResp)

        #parse
        search_result = {}
        if urlResp.has_key('taginfo') and urlResp['taginfo'].has_key('songlist'):
            tmp_list = urlResp['taginfo']['songlist']
            if len(tmp_list) > 0:
                #从前song_page_size个随机取出一个
                song_index = random.randint(0, len(tmp_list)-1)
                #print 'song_index = %d' % song_index
                DebugPrint('song_index = %d' % song_index)
                songid = tmp_list[song_index]['song_id']
                search_result = self.search_song_byid(songid)

                song_list = []
                for song_tmp in tmp_list:
                    if song_tmp['song_id'] != songid:       #去掉刚才选择的歌曲
                        song_info = {}
                        song_info['fromLocal'] = False
                        song_info['songId'] = song_tmp['song_id']
                        song_info['tts'] = ''
                        song_list.append(song_info)
                search_result['list'] = song_list

        DebugPrint(search_result)
        return search_result


    #### search hot ####
    #https://openapi.baidu.com/rest/2.0/music/billboard/catalog获取榜单id
    def search_by_billid(self, bill_id):
        postUrl = ("https://openapi.baidu.com/rest/2.0/music/billboard/billlist?type=%d&access_token=%s&page_size=%d&page_no=1" %
                   (bill_id, self.__access_token, song_page_size))

        urlResp = urllib.urlopen(postUrl)
        urlResp = urlResp.read()
        urlResp = json.loads(urlResp)
        #print urlResp
        DebugPrint(urlResp)

        #parse
        search_result = {}
        if urlResp.has_key('billboard2') and urlResp['billboard2'].has_key('song_list'):
            tmp_list = urlResp['billboard2']['song_list']
            if len(tmp_list) > 0:
                #从前song_page_size个随机取出一个
                song_index = random.randint(0, len(tmp_list)-1)
                #print 'song_index = %d' % song_index
                DebugPrint('song_index = %d' % song_index)
                songid = tmp_list[song_index]['song_id']
                search_result = self.search_song_byid(songid)

                song_list = []
                for song_tmp in tmp_list:
                    if song_tmp['song_id'] != songid:       #去掉刚才选择的歌曲
                        song_info = {}
                        song_info['fromLocal'] = False
                        song_info['songId'] = song_tmp['song_id']
                        song_info['tts'] = ''
                        song_list.append(song_info)
                search_result['list'] = song_list

        DebugPrint(search_result)
        return search_result

    def search_hot(self):
        hot_bill_id = 2
        return self.search_by_billid(hot_bill_id)





import tornado.ioloop
import tornado.options
from tornado.options import define, options
define("query",default='薛之谦',help='query string',type=str)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    baiduTmp = BaiduAuth()
    #baiduTmp.get_access_token()

    baiduTest = BaiduMusicSearch()
    #baiduTest.search_common(options.query)
    #songinfo = baiduTest.search_song_byid('276867440')
    #print songinfo
    search_result = baiduTest.search_hot()
    DebugPrint(search_result)
    search_result = baiduTest.search_by_style('摇滚')
    DebugPrint(search_result)
    print options.query
    search_result = baiduTest.search_common(options.query)
    DebugPrint(search_result)


