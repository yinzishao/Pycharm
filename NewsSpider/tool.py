
# -*- coding: utf-8 -*-
__author__ = 'yinzishao'
import urllib2

afp = 'http://www.afp.com/'
searchurl ='http://www.afp.com/en/search/site/'

def write(path,content):
    with open(path,'w') as f:
        for i in content:
            f.write(i+'\n')

#得到链接的源代码
def geturl_con(url):
    try:
        response =urllib2.urlopen(url)
        html = response.read()
    except urllib2.HTTPError, e:
        print e.code
    return html