#coding=utf-8
import random

__author__ = 'yinzishao'
import cookielib
import urllib2
import urllib
import re
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getBaiduuid():
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    baiduMainUrl = "http://www.baidu.com/"
    resp =urllib2.urlopen(baiduMainUrl)
    # print resp.info()
    # for index,cookie in enumerate(cj):
    #     print index,":",cookie
    getTokenUrl ="https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&tt=1445257071916&class=login&gid=A7EF8F2-862A-45EC-8394-4BFF01A6914A&logintype=dialogLogin&callback=bd__cbs__1uit2x"
    getTokenResp = urllib2.urlopen(getTokenUrl)
    getTokenHtml = getTokenResp.read()
    # print getTokenHtml
    pattern = r'"token".:."(.{20,40})",'
    p =re.compile(pattern)
    searchresult = p.search(getTokenHtml)
    if searchresult==None:
        # print "没找到token"
        getBaiduuid()
        # SystemExit
    else:
        token = searchresult.group(1)
        print token
        staticpage = "http://www.baidu.com/cache/user/html/jump.html"
        baiduMainLoginUrl = "https://passport.baidu.com/v2/api/?login"
        post ={
            'charset'       : "utf-8",
            #'codestring'    : "",
            'token'         : token, #de3dbf1e8596642fa2ddf2921cd6257f
            'isPhone'       : "false",
            'index'         : "0",
            #'u'             : "",
            #'safeflg'       : "0",
            'staticpage'    : staticpage, #http%3A%2F%2Fwww.baidu.com%2Fcache%2Fuser%2Fhtml%2Fjump.html
            'loginType'     : "dialogLogin",
            'tpl'           : "mn",
            'callback'      : "parent.bd__pcbs__ts9p8c",
            'username'      : "1175739669@qq.com",
            'password'      : "312892289?",
            #'verifycode'    : "",
            'mem_pass'      : "on",
        }
        postData =urllib.urlencode(post)
        # print postData
        req = urllib2.Request(baiduMainLoginUrl,postData)
        req.add_header('Content-Type',"application/x-www-form-urlencoded")
        resp =urllib2.urlopen(req)
        # for index, cookie in enumerate(cj):
        #     print '[',index, ']',cookie;
        tiebaresp = urllib2.urlopen("http://tieba.baidu.com/")
        tiebahtml = tiebaresp.read().decode('GBK')
        # print tiebahtml










    """得到吧的主页链接"""
def get_barurl(name):
    url='http://tieba.baidu.com/f?kw='
    url=url+urllib.quote(str(name))
    return url

def add_sign(name,value):
    print name,value
    url='http://tieba.baidu.com/sign/add'
    data={
        'ie':'utf-8',
        'kw':name,
        'tbs':value
        }
    try:
        postData =urllib.urlencode(data)
        res=urllib2.Request(url,postData)  #转换成post需要的格式
        res.add_header('Content-Type',"application/x-www-form-urlencoded")
        result=urllib2.urlopen(res)
        return result.read().decode('utf-8')
    except:
        print("签到%s失败" %name)
        return 0

    """ 匹配贴吧的所有吧 """
def match_bar(string):
    result=[]
    a=r'title="(.+?)">\1</a></td>'
    a=re.compile(a)
    result=re.findall(a,string)
    return result

    """ 得到所有贴吧的结果"""
def get_all_bar():
    url='http://tieba.baidu.com/f/like/mylike?pn='
    page=1
    result=[]
    while(1):
        url2=url+str(page)
        print(url2)
        html=urllib2.urlopen(url2)
        html=html.read()
        html=html.decode('gbk')
        result+=match_bar(html)
        if(html.find("下一页") == -1):
            break
        page+=1
    # print result
    return result

def get_tbs(value):
        resultr = urllib2.urlopen(value)
        content = resultr.read().decode('utf-8')
        # 第一种匹配tbs 的方法
        tbsPattern =re.compile(r'PageData.tbs = "(.{20,35})"')
        # print(content)
        t =tbsPattern.search(content)
        # print t.group(1)
        # try:
        #     tbs =tbsPattern.search(content).group(1)
        if t !=None:
            tbs =t.group(1)
        else:
            # 第二种匹配tbs 的方法
            tbsPattern  =re.compile(r'\'tbs\':."(.{20,35})"')
            t =tbsPattern.search(content)
            tbs=t.group(1)
            print tbs
        # except Exception,e:
        #     pass


        # if type(tbs) ==NoneType:
        #     print "s"
        # print(tbs)
        return tbs

def add_all_sign(bars):
    for index,i in enumerate(bars):
        # print i
        barurl = get_barurl(i)
        tbs = get_tbs(barurl)
        result=add_sign(i,tbs)
        if result != 0 :
            print("%s吧 签到成功" % i)
        sptime=random.randint(5,10)
        time.sleep(sptime)



if __name__ == '__main__':
    getBaiduuid()
    bars=get_all_bar()
    add_all_sign(bars)



"""
一些笔记:
    利用unquote解url的原始地址
    将空格编码为%20：urllib.quote
    urllib.quote(string[, safe])
    将空格编码为加号’+’：urllib.quote_plus
    urllib.quote_plus(string[, safe])
"""
def getunquote():
    encodedUrl = "http%3A%2F%2Fwww.baidu.com%2Fcache%2Fuser%2Fhtml%2Fjump.html";
    decodedUrl = urllib.unquote(encodedUrl);
    print "encodedUrl=\t%s\r\ndecodedUrl=\t%s"%(encodedUrl, decodedUrl);