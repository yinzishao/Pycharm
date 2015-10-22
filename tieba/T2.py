# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys,time,re,urllib.parse,urllib.request,http.cookiejar,random,math,os.path,hashlib,json,binascii,threading

"""cookie"""
cookie=http.cookiejar.LWPCookieJar()
#cookie.load('f:/cookie.txt',True,True)
chandle=urllib.request.HTTPCookieProcessor(cookie)
"""获取数据"""
def getData(url):
    r=urllib.request.Request(url)
    opener=urllib.request.build_opener(chandle)
    u=opener.open(r)
    #chandle.cookiejar.save('f:/cookie.txt',True,True)
    data=u.read()
    try:
        data=data.decode('utf-8')
    except:
        data=data.decode('gbk','ignore')
        return data
def postData(url,data):
    data=urllib.parse.urlencode(data);data=bytes(data,'utf-8')
    r=urllib.request.Request(url,data)
    opener=urllib.request.build_opener(chandle)
    u=opener.open(r)
    #chandle.cookiejar.save('f:/cookie.txt',True,True)
    data=u.read()
    try:
        data=data.decode('utf-8')
    except:
        data=data.decode('gbk','ignore')
        return data
def login(name,pwd):
    url='http://www.baidu.com'
    getData(url)
    par={
    "apiver":'v3',
    "callback":'bd__cbs__oug2fy',
    "class":'login',
    "logintype":'dialogLogin',
    "tpl":'tb',
    "tt":'1385013373144'
    }
    url='https://passport.baidu.com/v2/api/?getapi&%s' % urllib.parse.urlencode(par)
    token=re.findall('"token" : "(.*?)"',getData(url))[0]
    par.update({"isphone":'false',"username":name,"token":token})
    url='https://passport.baidu.com/v2/api/?logincheck&?%s' % urllib.parse.urlencode(par)
    data={
    "charset":'GBK',
    "mem_pass":'on',
    "password":pwd,
    "ppui_logintime":'1612376',
    "quick_user":'0',
    "safeflg":'0',
    "splogin":'rate',
    "u":'http://tieba.baidu.com/'
    }
    url='https://passport.baidu.com/v2/api/?login'
    par.update(data)
    bdu=re.findall('hao123Param=(.*?)&',postData(url,par))[0]
    par={
    "bdu":bdu,
    "t":'1385013373144'
    }
    url='http://user.hao123.com/static/crossdomain.php?%s' % urllib.parse.urlencode(par)
    getData(url)
    print(json.loads(getData('http://tieba.baidu.com/f/user/json_userinfo')))
    """------输入帐号密码------"""
    login('帐号','密码')

login('1175739669@qq.com','')