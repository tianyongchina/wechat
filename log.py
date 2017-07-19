#!/usr/bin/env python
#coding=utf-8

import os
import logging
from logging.handlers import RotatingFileHandler
log_file_name = "./logs/test_pid_" + str(os.getpid()) + ".log"

#################################################################################################
log_level = logging.DEBUG
logging.basicConfig(level = log_level,
        format = '%(asctime)s %(filename)s[line:%(lineno)d] [%(levelname)s] %(message)s',
        datefmt = '%a, %d %b %Y %H:%M:%S',
        filename = log_file_name,
        filemod = 'w')

#################################################################################################
#定义一个StreamHandler，将DEBUG级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
#console = logging.StreamHandler()
#console.setLevel(logging.NOTSET)
#formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] [%(levelname)s] %(message)s')
#console.setFormatter(formatter)
#logging.getLogger('').addHandler(console)


#################################################################################################
#定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大100M
#Rthandler = RotatingFileHandler(log_file_name, maxBytes = 10*1024*1024, backupCount = 5)
#Rthandler.setLevel(logging.NOTSET)
#formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] [%(levelname)s] %(message)s')
#Rthandler.setFormatter(formatter)
#logging.getLogger('').addHandler(Rthandler)

def debug(msg):
    logging.debug(msg)

def info(msg):
    logging.info(msg)

def warning(msg):
    logging.warning(msg)

def error(msg):
    logging.error(msg)

if __name__ == '__main__':
    debug('debug test')
    info('info test')
    warning('warning test 你好')
    error('error %d' % 12)
    dic = {'key1': '你好', 'key2': 'val3'}
    debug("===>>> %s"%(dic))
    debug("===>>11111> "% dic)
