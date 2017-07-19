#!/usr/bin/python
# -*- coding: utf-8 -*-


import tornado.web
import hashlib
import reply
import receive
import json
import thread

import tornado.gen
from tornado.concurrent import run_on_executor
# 这个并发库在python3自带在python2需要安装sudo pip install futures
from concurrent.futures import ThreadPoolExecutor

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('../')
import log

from dataproc.datacenter import DataCenter
from dataproc.datadefine import Xdata
from wxclient import WeixinClient
from sign import Sign
from nlpproc import NlpProc

from time import strftime,gmtime
from datetime import datetime
from iflytek import IflyTek
#import pdb
#pdb.set_trace()

test_urlhead = 'http://www.test.com'
test_show_urlhead = 'http://www.test.com/wx/show'
test_weixin_token = 'test'
test_weixin_appid = 'wx5b7fafa23bf1387b'
ai_data_file_name = 'data.json'
test_split_str = "@&@"

def time_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def sql_trans(data):
    #data = data.replace("\\", "\\\\")
    data = data.replace('"', '\\"')
    data = data.replace("'", "\\'")
    data = data.replace("%", "%%")
    return data 

class PerformanceTest(tornado.web.RequestHandler):
    def get(self):
        self.write("performance test.")

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        '''
        lst = ["python","www.itdiffer.com","qiwsir@gmail.com"]
        self.render("index.html", info=lst)
        '''
        # get userid by id
        body = self.request.body
        print "============>>>>>>>>>>>>>>>>>>>>start"
        print body
        print "============>>>>>>>>>>>>>>>>>>>>end."
        res = DataCenter().get_data_by_id(int(body['id']))
        _userid = res[0]['userid']
        # get sign ticket for weixin jsapisdk
        ticket = DataCenter().get_jsapi_ticket()
        urlall = self.request.uri
        #print self.request.path        /wx/show
        #print self.request.uri         /wx/show?id=oLN9QxI-YpdNJkSIXQkppJDHuvZM&showid=15
        sign = Sign(ticket, test_urlhead + urlall)
        sign_data = sign.sign()
        #print 'weixin_JSAPI_ticket: '
        #print sign_data
        log.info('weixin_JSAPI_ticket: %s'%(sign_data))
        timestamp = sign_data['timestamp']
        nonceStr = sign_data['nonceStr']
        signature = sign_data['signature']

        # get_param id
        title_info = '标题：人工智能的未来在哪里'
        all_info = ["先看一下这个情况，中国出口到全球，其中英国占中国出口的3%左右，但是退欧之后，我们看到整个的英镑是狂跌。",
                "另外大家现在寻求一个避险的港湾，避险的港湾在哪里呢？美元是第一，其次是日元，然后是黄金，最后就是美国的国债，其他一些资产有很大风险性。",
                "不过很多分析是有错误的，这么多专家、这么多经济学家、这么多非常能干的交易员，他们的分析判断在这个事件发生之前是不靠谱的。",
                "所以如果人工智能在未来的15年能帮助人类分析、判断，规避风险，我觉得这会是一个突破。",
                "我在美国的硕士学位就是和机器人有关的，我们学的是简单的控制，是你控制一个机器手，或者机器做的事情，和现在谈的人工智能概念差别还是很大的。",
                "另外一方面，我们现在看的人工智能，有人尖叫，有人担忧。其实还不到这个程度，因为我们现在看到的人工智能，无论是AlphaGo还是其他的人工智能，我觉得还是属于第一智能的状态。",
                "文章全文到此结束"]
        sub_info = ["主题1：人工智能的新时代即将到来",
                "主题2：人工智能到底能做什么",
                "主题3：人工智能的道路还很漫长"]
        self.render("index.html", title=title_info, allinfo=all_info, subjects=sub_info, author="", \
                createtime="2017-03-01 00:00:00", appid=test_weixin_appid, timestamp=timestamp, nonceStr=nonceStr, signature=signature, userid=_userid)


class WxShowHandler(tornado.web.RequestHandler):
    def get(self):
        '''
        the import handle
        '''
        try:
            webData = self.request.body
            #print "WxShowHandler Get webdata is ", webData
            log.info("WxShowHandler Get webdata is %s" % (webData))

            id = self.get_argument('id', '')
            showidstr = self.get_argument('showid', '')
            if len(id) == 0 or len(showidstr) == 0:
                self.write('parameter error!')

            # get sign ticket for weixin jsapisdk
            ticket = DataCenter().get_jsapi_ticket()
            urlall = self.request.uri
            #print self.request.path        /wx/show
            #print self.request.uri         /wx/show?id=oLN9QxI-YpdNJkSIXQkppJDHuvZM&showid=15
            sign = Sign(ticket, test_urlhead + urlall)
            sign_data = sign.sign()
            #print 'weixin_JSAPI_ticket: '
            #print sign_data
            log.info('weixin_JSAPI_ticket: %s'%(sign_data))
            timestamp = sign_data['timestamp']
            nonceStr = sign_data['nonceStr']
            signature = sign_data['signature']

            # get_param id
            showid = long(showidstr)
            userdata = DataCenter().get_data_by_id(showid)
            if len(userdata) == 0:
                self.write("no data")
                return
            data_dict = userdata[0]
            #print data_dict
            log.debug(data_dict)

            title_info = data_dict['title']
            sub_info = data_dict['aidata'].split(test_split_str)
            all_info = data_dict['originaldata'].split(test_split_str)
            createtime = data_dict['createtime'].strftime('%Y-%m-%d %H:%M:%S')

            author = ''
            authorinfo = data_dict['author']
            datasource = data_dict['datasource']
            _userid = data_dict['userid']
            if authorinfo == '':
                author = datasource
            elif datasource == '':
                author = authorinfo
            else :
                author = authorinfo + ' | ' + datasource

            self.render("index.html", title=title_info, allinfo=all_info, subjects=sub_info, author=author, \
                    createtime=createtime, appid=test_weixin_appid, timestamp=timestamp, nonceStr=nonceStr, \
                    userid=_userid, signature=signature)
        except Exception, Argument:
            log.error(Argument)
            self.write(Argument)



class GetTicketHandler(tornado.web.RequestHandler):
    '''
    /wx/getjsapiticket
    '''
    def get(self):
        ticket = DataCenter().get_jsapi_ticket()
        sign = Sign(ticket, 'http://www.test.com/wx/getjsapiticket')
        sign_str =  sign.sign()
        #print 'weixin_JSAPI_ticket: '
        #print sign_str
        log.info('weixin_JSAPI_ticket: %s'%(sign_str))
        self.write(sign_str)


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

class WxHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            webData = self.request.body
            #print "Handle Get webdata is ", webData
            log.debug("Handle Get webdata is %s" % (webData))

            signature = self.get_argument('signature', '')
            timestamp = self.get_argument('timestamp', '')
            nonce = self.get_argument('nonce', '')
            echostr = self.get_argument('echostr', '')
            token = test_weixin_token

            if len(signature) == 0 or len(timestamp) == 0 or \
                    len(nonce) == 0 or len(echostr) == 0:
                        self.write('')

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            #print "handle/GET func: hashcode, signature: ", hashcode, signature
            log.debug("handle/GET func: hashcode, signature: %s, %s"%(hashcode, signature))
            if hashcode == signature:
                self.write(echostr)
            else:
                self.write('')
        except Exception, Argument:
            log.error(Argument)
            self.write(Argument)

    '''
    重要说明：虽然模仿了回调模式，但是由于proc_weixin_text函数还是同步阻塞的，所以并没有实现多客户异步访问的功能
    ****Tornado中将同步变异步的方法是：****
    ThreadPoolExecutor模块和run_on_executor装饰器。用法就是建立线程池，用run_on_executor装饰的函数即运行在其中线程中，从而从主线程中分离出来，达到异步的目的。
    类似的还有IOLoop.add_callback方法，延迟执行
    '''
    executor = ThreadPoolExecutor(4)
    #executor 是局部变量  不是全局的
    @run_on_executor
    def proc_weixin_text(self, toUser, fromUser, content):
        userdata = DataCenter().get_user(toUser)
        if 'http:' not in content and 'https:' not in content:
            if len(userdata) == 0:
                content = "Your user info is not in database.Please unsubscribe and subscribe again!"
            else:
                user_dict = userdata[0]
                #print user_dict
                log.debug(user_dict)
                if user_dict.has_key('id'):
                    userid = user_dict['id']
                func_str = content.split()

                if (len(func_str) > 1) and ('查询' in func_str[0]):
                    res = DataCenter().search_data_by_title(func_str[1:], userid)
                    if len(res):
                        backmsg = ("%s\n%s?id=%s&showid=%d") %(res[0].title.encode("UTF-8"), test_show_urlhead, toUser, res[0].id)
                        #print ("send back to weixin user:"), backmsg
                        log.debug("send back to weixin user: %s"%(backmsg))
                        content = backmsg
                    else:
                        content = '太深奥了，X无可奉告'
                        #content = 'Sorry, there is no data about your query. You could try other keyword.'
                elif content != "": #闲聊
                    answer = IflyTek().sch_text(content)
                    if answer != None:
                        #TODO
                        content = answer
                    else:
                        #TODO
                        #content = 'Sorry, i can\'t find any information about the key.'
                        content = '太深奥了，X无可奉告'
                else:
                    #content = 'Welcome to the test test. Please click this: http://www.test.com/'
                    content = '太深奥了，X无可奉告'

        else:
            #userdata = DataCenter().get_user(toUser)
            if len(userdata) == 0:
                content = "Your user info is not in database.Please unsubscribe and subscribe again!"
            else:
                user_dict = userdata[0]
                #print user_dict
                log.debug(user_dict)
                if user_dict.has_key('id'):
                    userid = user_dict['id']

                #get info from NLPTA
                urlinfo = content[content.find('http'):]  #取http后面的内容，避免前有特殊字符
                #print "NLPTA process begin......"
                log.info("NLPTA process begin......url: %s" %(urlinfo))
                nlprtn = NlpProc().retrieve_Info_From_URL(urlinfo)
                if nlprtn[0] != None and nlprtn[1] == 'NLP_TA_Success':
                    #for test
                    #with open(ai_data_file_name, "w") as f_output:
                        #f_output.write(nlprtn[0])

                    #parse result
                    #print "NLPTA process ok......"
                    log.info("NLPTA process ok......")
                    #nlpjson = json.loads(nlprtn[0], object_hook=_decode_dict)
                    jsonstrtmp = nlprtn[0]
                    #jsonstrtmp = jsonstrtmp.replace('%','%%')   #很重要，将字符串%转义，否则在插入数据库会出错
                    nlpjson = json.loads(jsonstrtmp)
                    #print nlpjson
                    log.debug(nlpjson)

                    #write to db, return new URL: title + URL
                    datatmp = Xdata()
                    datatmp.userid = userid
                    datatmp.title = sql_trans(nlpjson['title'].encode("UTF-8"))
                    datatmp.url = sql_trans(urlinfo) #url也有%等特殊字符
                    datatmp.datadesc = ''
                    datatmp.author = sql_trans(nlpjson['author'].encode("UTF-8"))
                    datatmp.datasource = sql_trans(nlpjson['source'].encode("UTF-8"))
                    datatmp.createtime = nlpjson['date'].encode("UTF-8")
                    datatmp.aidata = test_split_str.join(nlpjson['abstract']).encode("UTF-8")  #nlprtn[0].encode("UTF-8")      #直接存入智能处理的全部字符串，免得来回解析
                    datatmp.aidata = sql_trans(datatmp.aidata)
                    datatmp.originaldata = test_split_str.join(nlpjson['content']).encode("UTF-8")
                    datatmp.originaldata = sql_trans(datatmp.originaldata)
                    datatmp.addtime = time_now()
                    #datatmp.accesstime = time_now()  #'0000-00-00 00:00:00'
                    datatmp.accesstime = datatmp.addtime #'0000-00-00 00:00:00'
                    datatmp.flag = 1
                    addrtn = DataCenter().add_data(datatmp)

                    backmsg = ("%s\n%s?id=%s&showid=%d") %(datatmp.title, test_show_urlhead, toUser, addrtn)
                    #print ("send back to weixin user:"), backmsg
                    log.debug("send back to weixin user: %s" %(backmsg))
                    content = backmsg
                else:
                    #nlp error, return
                    #print "############NPLTA process error ", nlprtn[1]
                    log.warning("############NPLTA process error %s"%(nlprtn[1]))
                    content = nlprtn[1]
        return (content)

    def cb_proc_weixin_text(self, toUser, fromUser, content):
        replyMsg = reply.TextMsg(toUser, fromUser, content)
        #print "Handle post reply data is ", replyMsg.send()
        log.debug("Handle post reply data is %s"%(replyMsg.send()))
        self.write(replyMsg.send())
        self.finish()

    '''
    重要说明：通过新建一个线程来执行proc_weixin_text函数，保证proc_weixin_text_async的异步性
    '''
    def proc_weixin_text_async(self, toUser, fromUser, content, callback):
        thread.start_new_thread(self.proc_weixin_text,(toUser, fromUser, content, callback))

    '''
    使用@tornado.gen.coroutine ，只是将异步的回调方式改成了同步方式的代码，流程更清楚一点。
    '''
    '''
    使用@tornado.web.asynchronous，它主要设置_auto_finish为false，这样handler的get函数返回的时候tornado就不会关闭与client的连接。
    callback调用完成之后通过finish结束与client的连接。
    '''
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        try:
            webData = self.request.body
            #print "Handle Post webdata is ", webData
            log.debug("Handle Post webdata is %s" % (webData))
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                    content = recMsg.Content
                    res = yield self.proc_weixin_text(toUser, fromUser, content)
                    self.cb_proc_weixin_text(toUser, fromUser, res)

                elif recMsg.MsgType == 'voice':
                    content = recMsg.Content
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    #print "Handle post reply data is ", replyMsg.send()
                    log.debug("Handle post reply data is %s"%(replyMsg.send()))
                    self.write(replyMsg.send())
                    self.finish()
                elif recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    #print "Handle post reply data is ", replyMsg.send()
                    log.debug("Handle post reply data is %s" %(replyMsg.send()))
                    self.write(replyMsg.send())
                    self.finish()
                else:
                    #print "success or null"
                    log.debug("success or null")
                    self.write("success")
                    self.finish()
            elif isinstance(recMsg, receive.EventMsg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.Event == 'CLICK':
                    if recMsg.Eventkey == 'mpGuide':
                        content = 'building............'
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        #print "Handle post reply data is ", replyMsg.send()
                        log.debug("Handle post reply data is %s"%(replyMsg.send()))
                        self.write(replyMsg.send())
                        self.finish()
                elif recMsg.Event == 'subscribe':
                    # send to weixin
                    content = "Welcome to the test world.I'm the x,the special one.You can help us do a test.Please click this: http://www.test.com/"
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    #print "Handle post reply data is ", replyMsg.send()
                    log.debug("Handle post reply data is %s"%(replyMsg.send()))
                    postData = replyMsg.send()
                    if isinstance(postData, unicode):
                        postData = postData.encode('utf-8')
                    self.write(postData)
                    self.finish()

                    # get user info
                    user_info = WeixinClient().get_user_info(recMsg.FromUserName)
                    # add to db
                    # unionid = user_info['unionid'] #主要用于各种不同公众号之前的绑定关系。只有绑定开放平台之后才会有，先写''
                    unionid = ''
                    DataCenter().add_user(user_info['openid'], user_info['subscribe'], \
                            user_info['nickname'], user_info['sex'], \
                            user_info['headimgurl'], unionid)

                elif recMsg.Event == 'unsubscribe':
                    # send to weixin
                    content = "I'm very sorry,see you later!"
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    #print "Handle post reply data is ", replyMsg.send()
                    log.debug("Handle post reply data is %s"%(replyMsg.send()))
                    self.write(replyMsg.send())
                    self.finish()

                    # delete from db
                    DataCenter().del_user_by_openid(toUser)
                else:
                    #print "success or null"
                    log.debug("success or null")
                    self.write("success")
                    self.finish()
            else:
                #print "success or null"
                log.debug("success or null")
                self.write("success")
                self.finish()
        except Exception, Argment:
            #print "ERROR: throw exception: ", Argment
            log.error("ERROR: throw exception: %s" % (Argment.message))
            self.write(Argment.message)
            self.finish()

class WxInteractionHandler(tornado.web.RequestHandler):
    def get(self):
        data = self.get_argument('interaction').encode('utf-8')
        answer = IflyTek().sch_text(data)
        if answer == None:
            ans = "太深奥了，无可奉告".encode('utf-8')
        else:
            ans = answer.encode('utf-8')
        #print ans
        log.debug(ans)
        self.write(ans)
