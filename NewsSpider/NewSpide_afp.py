__author__ = 'yinzishao'
# -*- coding: utf-8 -*-
import urllib2
import re
from bs4 import BeautifulSoup
#得到链接的源代码
def geturl_con(url):
    try:
        response =urllib2.urlopen(url)
        html = response.read()
    except urllib2.HTTPError, e:
        print e.code
    return html

#得到链接的新闻链接
def findurl(html):
    soup =BeautifulSoup(html)
    res = soup.find_all('h3',class_='title')
    print res
    # print res.h3.a['href']
def hasnext(html):
    soup = BeautifulSoup(html)
    next = soup.find('li',class_='pager-next')  #找出下一页
    if next:
        return True
    else :
        return False

t = geturl_con('http://www.afp.com/en/search/site/21st-century%20maritime%20silk%20road/?page=1')
findurl(t)

if __name__ == '__main__':
    starurl ='http://www.afp.com/en/search/site/21st-century%20maritime%20silk%20road/?page='
    page =1
    html =geturl_con(starurl+str(page))
    findurl(html)

    while True:
        if hasnext(html):
            page =page+1
            html =geturl_con(starurl+str(page))

            print page
        else:
            break


