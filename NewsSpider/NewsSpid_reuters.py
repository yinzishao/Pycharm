#coding=utf-8
__author__ = 'yinzishao'

import urllib
import urllib2
from tool import *
import re
from bs4 import BeautifulSoup
surl = 'http://www.reuters.com/search/news?blob='
TOTALNUM=0


#输入关键词得到链接
def search(keyword):
    urlset = set()
    global TOTALNUM
    keywordchange=re.sub(r' ','+',keyword)  #转换成url所需格式
    furl =surl+keywordchange                #得到最终的url
    html = geturl_con(furl)
    # print html
    soup = BeautifulSoup(html)
    res =soup.find_all('h3',class_='search-result-title')
    TOTALNUM =soup.find('span',class_='search-result-count search-result-count-num').string  #得到结果的总数
    print TOTALNUM
    # print len(res)

    for r in res:
        urlset.add(str(r.a['href']))  #提取链接

    # print len(uset)
    #从第二页开始就要从js中获得链接
    i=2
    print  TOTALNUM
    while (((i-1)*10)<int(TOTALNUM)):
        urlset=urlset|searchjs(keyword,i)

        i=i+1
        print  TOTALNUM
        print i

    print len(urlset)

    with open('reuters.txt','w')as r:
        for url in urlset:
            r.writelines(url+'\n')

def searchjs(keyword,num):
    headurl = 'http://www.reuters.com/assets/searchArticleLoadMoreJson?blob='+\
              urllib.quote(keyword)\
              +'&bigOrSmall=big&articleWithBlog=true&sortBy=&dateRange=&numResultsToShow=10&pn='\
              +urllib.quote(str(num))+'&callback=addMoreNewsResults'
    html =geturl_con(headurl)
    # print html
    return geturl(html)
    # soupjs = BeautifulSoup(html)

#得到js中的链接 与Totalnum

def geturl(html):
    global TOTALNUM
    numre =re.compile(r'totalResultNumber: (.*?),')
    urlre =re.compile(r'href: "(.*)",')
    num =re.search(numre,html)   #得到结果的总数
    url =re.findall(urlre,html)  #得到链接的set集合
    urlset = set(url)
    num = num.group(1)

    if num < TOTALNUM :
            TOTALNUM = num
            print TOTALNUM
            return urlset
    else:
            return urlset

search('21st-century maritime silk road')