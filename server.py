#!/usr/bin/env python
#coding:utf-8

import json
import tornado.autoreload
import tornado.ioloop
import tornado.options
import tornado.httpserver
from application import application
from wxclient import WeixinClient
from dataproc.datacenter import DataCenter
from nlpproc import NlpProc
from iflytek import IflyTek
from himalaya import Himalaya

import log
import time
import datetime
import signal
import sys

period = 1800 * 1000 * 3  # every 1.5h

from tornado.options import define, options
define("port",default=80,help="run on th given port",type=int)

def signal_handler(sign, stack):
    if sign == signal.SIGINT:
        print "Got a SIGINT signal, the program ready to quit."
        sys.exit()
    else:
        print "Got a signal but not deal, signal:%d" % sign

def like_cron():
    #print datetime.datetime.now()
    log.debug(datetime.datetime.now())

def main():
    # deal Ctrl-C
    signal.signal(signal.SIGINT, signal_handler)

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)

    #启动单进程
    http_server.listen(options.port)

    #启动多进程监听(进程个数为机器核心个数)
    #http_server.bind(options.port)
    #http_server.start(0)

    #print 'Development server is running at http://127.0.0.1:%s/' % options.port
    #print 'Quit the server with Control-C'
    log.info('Development server is running at http://127.0.0.1:%s/' % options.port)
    log.info('Quit the server with Control-C')

    # nlpproc init
    nlp_global_obj = NlpProc()
    nlp_global_obj.init_nlpta()

    # datacenter init
    data_global_obj = DataCenter()
    data_global_obj.connect_db("127.0.0.1:3306",'testdb', 'root', 'password')

    # log in iflytek
    ifly_tek = IflyTek()

    # start get access token timer
    get_access_token_instance = WeixinClient()
    get_access_token_instance.get_access_token()   #get first time
    tornado.ioloop.PeriodicCallback(get_access_token_instance.get_access_token, period).start()  # start scheduler
    
    get_himalaya_access_token_ins = Himalaya()
    tornado.ioloop.PeriodicCallback(get_himalaya_access_token_ins.get_access_token, period).start()

    # test
    #tornado.ioloop.PeriodicCallback(like_cron, 10000).start()  # start scheduler

    # start tornado ioloop
    tornado.ioloop.IOLoop.instance().start()


if __name__=="__main__":
    #test()
    main()

