#!/usr/bin/env python #coding:utf-8
import tornado.web
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MyStaticFile(tornado.web.StaticFileHandler):  
    def set_extra_headers(self, path):  
        self.set_header("Cache-control", "no-cache")
