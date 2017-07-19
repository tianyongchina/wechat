#!/usr/bin/env python
#coding:utf-8

import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')

from handler.index import IndexHandler
from handler.index import GetTicketHandler
from handler.index import WxHandler
from handler.index import WxShowHandler
from handler.index import WxInteractionHandler
from handler.index import PerformanceTest
from handler.static import MyStaticFile
from handler.nlu import TextCmdHandler
from handler.broadcast import CollectionHandler
from handler.broadcast import RecommendHandler
from handler.broadcast import SongHandler

url=[
    #(r'/', IndexHandler),
    (r'/wx', WxHandler),
    (r'/wx/show', WxShowHandler),
    (r'/wx/getjsapiticket', GetTicketHandler),
    (r'/wx/interaction', WxInteractionHandler),
    (r'/textCmd', TextCmdHandler),
    (r'/collection/(.*)', CollectionHandler),
    (r'/recommendation', RecommendHandler),
    (r'/song/info', SongHandler),
    (r'/performance_test', PerformanceTest),

    #test, if use nginx , not use these
    (r'/(.*)', MyStaticFile, {'path':os.path.dirname(os.path.realpath(__file__))+'/static'}),
    (r'/wx/(.*)', MyStaticFile, {'path':os.path.dirname(os.path.realpath(__file__))+'/static'}),
    (r'/wx/show/(.*)', MyStaticFile, {'path':os.path.dirname(os.path.realpath(__file__))+'/static'}),

]
