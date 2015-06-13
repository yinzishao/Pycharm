__author__ = 'yinzishao'
#coding=utf-8
import urllib2
import re
def _crawl_cnn(keywork):

    page =1
    npp =10#每一页数
    start =1
    keywork = re.sub(r' ','%2B',keywork)
    print keywork
    urls = 'http://searchapp.cnn.com/search/query.jsp?'
    # page=1&npp=10&start=1&text=new%2Bsilk%2Broad&type=all&bucket=true&sort=relevance&collection=STORIES%2C&csiID=csi4'
    urle = 'page=%d&npp=%d&start=%d&text=%s&type=all&bucket=true&sort=relevance&collection=STORIES%%2C&csiID=csi4'%(int(page),int(npp),int(start),keywork)
    print urle
    url = urls+urle
    response = urllib2.urlopen(url)
    html = response.read()
    print html

if __name__ =='__main__':
    _crawl_cnn('new silk road')