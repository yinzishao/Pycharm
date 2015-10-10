# -*- coding: utf-8 -*-
import cookielib
import re
import time
import os
import random
import urllib2
import urllib
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

cj = cookielib.CookieJar();
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
# urllib2.install_opener(opener);
# reqReturn = urllib2.urlopen(URL_BAIDU_INDEX);

# cookiejar=http.cookiejar.LWPCookieJar('tieba')
# CookieHandle=urllib.request.HTTPCookieProcessor(cookiejar)
# opener=urllib.request.build_opener(CookieHandle,urllib.request.HTTPHandler)


def make_cookie(name,value):
    cookie=cookielib.Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain="baidu.com",
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None
    )
    return cookie

def get_barurl(name):
    url='http://tieba.baidu.com/f?kw='
    url=url+urllib.quote(str(name))
    return url

def add_sign(name,value):
    url='http://tieba.baidu.com/sign/add'
    data={
        'ie':'utf-8',
        'kw':name,
        'tbs':value
        }
    try:
        result=opener.open(url,urllib.urlencode(data))  #转换成post需要的格式
        return result.read().decode('utf-8')
    except:
        print("签到%s失败" %name)
        return 0
def match_bar(string):
    result=[]
    a=r'title="(.+?)">\1</a></td>'
    a=re.compile(a)
    result=re.findall(a,string)
    return result

def get_all_bar():
    url='http://tieba.baidu.com/f/like/mylike?pn='
    page=1
    result=[]
    while(1):
        url2=url+str(page)
        print(url2)
        html=opener.open(url2)
        html=html.read()
        html=html.decode('gbk')
        result+=match_bar(html)
        if(html.find("下一页") == -1):
            break
        page+=1
    return result

def get_tbs(value):
        resultr = opener.open(value)
        content = resultr.read().decode('utf-8')
        tbsPattern =re.compile(r'PageData.tbs = "(.{20,35})"')
        # print(content)
        tbs =tbsPattern.search(content).group(1)
        # print(tbs)
        return tbs

def add_all_sign(bars):
    for index,i in enumerate(bars):
        barurl = get_barurl(i)
        tbs = get_tbs(barurl)
        result=add_sign(i,tbs)
        if result != 0 :
            print("%s吧 签到成功" % i)
        sptime=random.randint(5,10)
        time.sleep(sptime)


BDUSS='VAxSjlTeDdZcEVhYW5iVHgyNTZaMjhmVEZ2dnpSUzVJczNXSHRQZDFUejlJSDFWQVFBQUFBJCQAAAAAAAAAAAEAAACVjlA13-3YraCRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP2TVVX9k1VVY'#此处请修改为自己的BDUSS
cookie=make_cookie('BDUSS',BDUSS)
cj.set_cookie(cookie)


bars=get_all_bar()
add_all_sign(bars)


# tbsPattern = re.compile('"tbs" value=".{20,35}"')
#
# def signIn(tieBaName):
#     '''签到'''
#     # 获取页面中的参数tbs
#     conn1 = HTTPConnection("tieba.baidu.com", 80)
#     queryStr1 = urllib.parse.urlencode({"kw": tieBaName})
#     conn1.request("GET", "/mo/m?" + queryStr1, "", headers)
#     html = conn1.getresponse().read().decode()
#     tbs = tbsPattern.search(html).group(0)[13:-1]
#     # 签到
#     conn2 = HTTPConnection("tieba.baidu.com", 80)
#     body = urllib.parse.urlencode({"kw":tieBaName, "tbs":tbs, "ie":"utf-8"})
#     conn2.request("POST", "/sign/add" , body , headers)
#     resp2 = conn2.getresponse()
#     data = json.loads((gzip.decompress(resp2.read())).decode())
#     return data