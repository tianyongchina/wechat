## 依赖安装和使用说明 ##
#### 依赖安装 ####
安装python,vim,mysql,tornado库  
安装pip支持  
安装python-mysqldb支持  
安装textrank4zh和lxml支持（智能处理需要）  
安装tornado的异步处理库  
```Bash
apt-get update
apt-get -y install python vim
apt-get -y install mysql-server mysql-client
apt-get install python-setuptools
easy_install pip
pip install tornado
apt-get install python-mysqldb
pip install lxml
pip install textrank4zh
pip install futures
```
运行
```Bash
python server.py
```

#### 微信公众号demo使用方法 ####
1、搜索关注公众号“物灵LingX”；  
2、查看其它公众号的文章，点击右上角，选择“复制链接”；  
3、进入“物灵LingX”公众号，粘贴刚才的信息，发送。公众号会回复一条“主题+链接”的信息。点击链接，进入的页面会显示文章的全部文字和摘要信息。同时会自动语音播报文章的全部内容，正在播报的文字页面上会以红色标识出来；  
4、页面最下方可以进行播报控制。在输入框输入文字后，发送即可。也可以切换成语音控制，内容和文字一样。目前采用微信语音识别，响应比较慢，效果不是很好，后续改进。  
a)播报上一条。输入文字可以是：previous，up，上一，上面，前一，前面  
b)播报下一条。输入文字可以是：next，down，下一，下面，后一，后面  
c)播报摘要。输入文字可以是：summary，摘要，概要，主题，简介，简单点  
d)播报全文。输入文字可以是：all，全文，全部，所有，详细点  
e)继续播报。输入文字可以是：continue，继续，接着  
f)重新播报。输入文字可以是：begin，重头来，重新  
g)重复播报。输入文字可以是：repeat，重复  
下面两条因为讯飞SDK的BUG，暂不支持  
h)音量控制。输入文字可以是：upper,大点声，声音大一点，lower，小点声，声音小一点  
i)语速控制。输入文字可以是：faster,快点，快一点，slower，慢点，慢一点  


[测试网址](http://projectx.ling.cn)  
![](http://projectx.ling.cn/logo.jpg)  