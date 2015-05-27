__author__ = 'yinzishao'
# -*- coding: utf-8 -*-
import urllib2
import re
from tool import *
from bs4 import BeautifulSoup
#得到链接的新闻链接
def findurl(html):
    soup =BeautifulSoup(html)
    res = soup.find_all('h3',class_='title')
    print len(res)
    uset =set()
    for r in res:
         uset.add(afp+str(r.a['href']))
    return uset

#判断是否有下一页
def hasnext(html):
    soup = BeautifulSoup(html)
    next = soup.find('li',class_='pager-next')  #找出下一页
    if next:
        return True
    else :
        return False

#keyword搜索关键词,得到路径
def geturl(keyword):
    uset= set()
    res = re.sub(r' ','%20',keyword)
    last ='/?page='
    starurl = searchurl+res+last     #得到路径
    page =1
    rl =starurl+str(page)
    print rl
    html =geturl_con(rl)
    temp =findurl(html)
    # print temp
    # print uset
    # print uset|temp
    # print len(findurl(html))
    uset =uset|findurl(html)


    while True:
        if hasnext(html):
            page =page+1
            rl =starurl+str(page)
            # print rl
            html =geturl_con(rl)
            uset =uset|findurl(html)
            print page
            print len(uset)
        else:
            break

    return uset

if '__main__' == __name__:
    a=geturl('21st-century maritime silk road')
    b=geturl('silk road economic belt')
    c=a&b
    print len(c)
    # write('apfurl.txt',urlset)

