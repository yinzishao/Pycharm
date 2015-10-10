'''
Created on 2014-2-20
 
@author: Vincent
'''
import urllib.parse
import gzip
import json
import re
from http.client import HTTPConnection
from htmlutils import TieBaParser
import httputils as utils
 
# 请求头
headers = dict()
headers["Connection"] = "keep-alive"
headers["Cache-Control"] = "max-age=0"
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36"
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["Accept-Encoding"] = "gzip,deflate,sdch"
headers["Accept-Language"] = "zh-CN,zh;q=0.8"
headers["Cookie"] = ""
 
# cookie
cookies = list()
 
# 个人信息
userInfo = {}
 
def login(account, password):
    '''登录'''
    global cookies
    headers["Host"] = "wappass.baidu.com"
    body = "username={0}&password={1}&submit=%E7%99%BB%E5%BD%95&quick_user=0&isphone=0&sp_login=waprate&uname_login=&loginmerge=1&vcodestr=&u=http%253A%252F%252Fwap.baidu.com%253Fuid%253D1392873796936_247&skin=default_v2&tpl=&ssid=&from=&uid=1392873796936_247&pu=&tn=&bdcm=3f7d51b436d12f2e83389b504fc2d56285356820&type=&bd_page_type="
    body = body.format(account, password)
    conn = HTTPConnection("wappass.baidu.com", 80)
    conn.request("POST", "/passport/login", body, headers)
    resp = conn.getresponse()
    cookies += utils.getCookiesFromHeaders(resp.getheaders())
    utils.saveCookies(headers, cookies)
    # 登录成功会返回302
    return True if resp.code == 302 else False
     
 
def getTieBaList():
    '''获取已关注的贴吧列表'''
    conn = HTTPConnection("tieba.baidu.com", 80)
    conn.request("GET", "/mo/m?tn=bdFBW&tab=favorite", "", headers)
    resp = conn.getresponse()    
    tieBaParser = TieBaParser()
    tieBaParser.feed(resp.read().decode())
    tbList = tieBaParser.getTieBaList()
    return tbList
     
 
def getSignInfo(tieBaName):
    '''获取贴吧签到信息'''
    queryStr = urllib.parse.urlencode({"kw":tieBaName, "ie":"utf-8", "t":0.571444})
    conn = HTTPConnection("tieba.baidu.com", 80)
    conn.request("GET", "/sign/loadmonth?" + queryStr, "", headers)
    data = gzip.decompress(conn.getresponse().read()).decode("GBK")
    signInfo = json.loads(data)
    return signInfo
     
      
tbsPattern = re.compile('"tbs" value=".{20,35}"')
 
def signIn(tieBaName):
    '''签到'''
    # 获取页面中的参数tbs
    conn1 = HTTPConnection("tieba.baidu.com", 80)
    queryStr1 = urllib.parse.urlencode({"kw": tieBaName})
    conn1.request("GET", "/mo/m?" + queryStr1, "", headers)
    html = conn1.getresponse().read().decode()
    tbs = tbsPattern.search(html).group(0)[13:-1]
    # 签到
    conn2 = HTTPConnection("tieba.baidu.com", 80)
    body = urllib.parse.urlencode({"kw":tieBaName, "tbs":tbs, "ie":"utf-8"})
    conn2.request("POST", "/sign/add" , body , headers)
    resp2 = conn2.getresponse()
    data = json.loads((gzip.decompress(resp2.read())).decode())
    return data
     
 
def getUserInfo():
    '''获取个人信息'''
    headers.pop("Host")
    conn = HTTPConnection("tieba.baidu.com", 80)
    conn.request("GET", "/f/user/json_userinfo", "", headers)
    resp = conn.getresponse()
    data = gzip.decompress(resp.read()).decode("GBK")
    global userInfo
    userInfo = json.loads(data)
 
 
if __name__ == "__main__":
    account = input("请输入帐号:")
    password = input("请输入密码:") 
    
    ok = login(account, password)
    if ok:
        getUserInfo()
        print(userInfo["data"]["user_name_weak"] + "~~~登录成功", end="\n------\n")
        for tb in getTieBaList():
            print(tb + "吧:")
            signInfo = signIn(tb)
            if signInfo["no"] != 0:
                print("签到失败!")
                print(signInfo["error"])
            else:
                print("签到成功!")
                print("签到天数:" + str(signInfo["data"]["uinfo"]["cout_total_sing_num"]))
                print("连续签到天数:" + str(signInfo["data"]["uinfo"]["cont_sign_num"]))
            print("------") 
    else:
        print("登录失败")