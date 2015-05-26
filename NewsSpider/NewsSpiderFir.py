# -*- coding: utf-8 -*-
__author__ = 'yinzishao'

import urllib2
import re

#根据输入的页数爬取其对应链接爬取
def getallurl():
    allurl =set()
    urltemp =set()
    for i in range(10):
        urltemp=urlspider(i*10)
        if urltemp==[]:       #爬不到链接断开
            break
        else:
            allurl = allurl | urltemp

    #写入文档
    urlpath ='silkurl.txt'
    with open(urlpath,'w') as f:
        for i in allurl:
            f.write(i+'\n')

#爬取页数为snum的数量

def urlspider(snum):
    starnum = snum
    url ='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=10&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=cb6ef4de1f03dde8c26c6d526f8a1f35&start='+str(starnum)+\
         '&cx=004830092955692134028:an6per91wyc&q=silk%20road&as_sitesearch=huffingtonpost.com&googlehost=www.google.com'

    # url='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwS'\
    #          +'G1gunmMikTzQqY&rsz=10&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=cb6ef4d'\
    #          +'e1f03dde8c26c6d526f8a1f35&start='+str(starnum)+'&cx=004830092955692134028:an6per91wyc&q=21st-century%'\
    #          +'20maritime%20silk%20road&as_sitesearch=huffingtonpost.com&googlehost=www.google.com'

    response = urllib2.urlopen(url)
    html = response.read()
    a=r'"url":"([^"]*?.html)"'
    a=re.compile(a)
    result = re.findall(a,html)
    # print result
    return set(result)





def readurl(url):
    pass

# urlspider(0)
getallurl()
# print len(urlspider(0)|urlspider(10))


