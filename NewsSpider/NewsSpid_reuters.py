#coding=utf-8
__author__ = 'yinzishao'

import urllib
import urllib2
from tool import *
import re
from bs4 import BeautifulSoup
surl = 'http://www.reuters.com/search/news?blob='

def search(keyword):


    keyword=re.sub(r' ','+',keyword)  #转换成url所需格式
    furl =surl+keyword                #得到最终的url
    html = geturl_con(furl)
    # print html
    soup = BeautifulSoup(html)
    res =soup.find_all('h3',class_='search-result-title')
    num =soup.find('span',class_='search-result-count search-result-count-num').string  #得到结果的总数
    print num
    # print len(res)
    uset = set()
    for r in res:
        uset.add(str(r.a['href']))  #提取链接

    # print len(uset)
    return uset

def searchjs(keyword):
    headurl = 'http://www.reuters.com/assets/searchArticleLoadMoreJson?blob='+\
              urllib.quote(keyword)\
              +'&bigOrSmall=big&articleWithBlog=true&sortBy=&dateRange=&numResultsToShow=10&pn=6&callback=addMoreNewsResults'
    html =geturl_con(headurl)
    print html

search('21st-century maritime silk road')