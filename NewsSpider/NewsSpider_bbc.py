#coding=utf-8
import ConnectedSQL

__author__ = 'yinzishao'
import urllib2
from bs4 import BeautifulSoup
import re
import types
allurl= set()
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#爬取结果总数
def extractTotalnum(html):
    result = re.search(r'data-total-results="(.*?)"',html)
    if (type(result) != types.NoneType):
        return result.group(1)
    else:
        return False
#爬起结果url
def extractUrl(html):
    # print html
    result = re.findall(r'<h1\sitemprop="headline"><a\shref="(.*?)"',html)
    # print result
    if len(result)>0:
        for url in result:
             allurl.add(url)

    # for url in result:
    #     print url.group(1)
# def extractTime(html):
#     soup =BeautifulSoup(html)
#     result = soup.find('time')
#     print result.get_text().strip()

#根据关键词爬取所有链接
def crawl_bbc(keywork):
    keywork = re.sub(' ','+',keywork)
    page = 1
    totalnum='100'
    while((page-1)*10<int(totalnum)):
        print page
        retry =3
        while(retry>0):
            try:

                url = 'http://www.bbc.co.uk/search/more?page=%d&q=%s&sa_f=search-serp&filter=news'%(page,keywork)
                # print url
                response = urllib2.urlopen(url)
                html = response.read()
                # print html
                totalnum = extractTotalnum(html)
                extractUrl(html)
                # print url
                break
            except Exception,e:
                print e
                retry -=1

                continue
            finally:page+=1
    print len(allurl)
    writeurl()

#把allurl 链接写进txt

def writeurl(path='bbc_allurl.txt'):
    with open(path,'w') as bw:
        with open('bbc_newurl.txt','w') as bnw:
            for url in allurl:
                bw.write(url+'\n')
                if  url.find('/news/')!=-1:
                    bnw.write(url+'\n')
                    print url

def extractContent(html,i=1):
    print i,'.'
    soup = BeautifulSoup(html)
    title =soup.find('h1',class_='story-body__h1')
    if type(title) is types.NoneType:
        title =None
    else:
        title = title.get_text().strip()
    print title
    author =soup.find('span',class_='byline__name')
    if type(author) is types.NoneType:
        author =None
    else:
        author =author.get_text().strip()
    print author

    # r = re.compile(r'date\sdate--v\d')
    # time =soup.find('div',class_=re.compile(r'date date--v2'))

    t =soup.find('div',class_='story-body')
    time =t.find(True,{'data-seconds':True})
    if type(time) is types.NoneType:
        time =None
    else:
        time =time.get_text().strip()

    print time

    content = soup.find('div',class_=['story-body__inner','map-body'])
    if type(content)is types.NoneType:
        content =None
    else:
        sub_fig = re.compile(r'<figure(\s|\S)*?</figure>')
        sub_scr = re.compile(r'<script(\s|\S)*?</script>')
        sub_jian = re.compile(r'<(\s|\S)*?>')
        sub_huanhang =re.compile(r'\n')
        content = re.sub(sub_fig,' ',str(content))
        content = re.sub(sub_scr,' ',str(content))
        content = re.sub(sub_jian,' ',str(content))
        content = re.sub(sub_huanhang,' ',str(content))
    print content


    l =[title,author,time,content]
    return l
def readurl(path='bbc_newurl.txt'):
    with open(path,'r') as br:
        urls = br.readlines()
    i =1
    contentlist =list()
    with open('bbc_contetn.txt','w') as bbcw:
        for url in urls:
            retry =3
            while retry>0:
                try:
                    response = urllib2.urlopen(url)
                    html = response.read()
                    l=extractContent(html,i)
                    l.insert(0,url.strip())
                    bbcw.write(str(i)+'.\n')
                    for a in l:
                        # print a
                        bbcw.write(str(a)+'\n')
                    contentlist.append(l)
                    print len(contentlist)

                    break
                except Exception,e:
                    print e
                    retry -=1
                    continue
            i+=1

#上传数据
def process_bbc(path='bbc_contetn.txt'):
    with open(path,'r') as r:
        line =r.readline()
        while(line):
            url =r.readline()
            title =r.readline()
            author = r.readline()
            time = r.readline()
            content = r.readline()
            l =[url,title,author,time,content]
            ConnectedSQL.commit_data(l)
            # print l
            line =r.readline()

if __name__ =='__main__':
    # _crawl_bbc('silk road')
    # readurl()
    process_bbc()
    # response = urllib2.urlopen('http://www.bbc.com/news/world-asia-china-19328092')
    # html = response.read()
    # extractContent(html)

    # extractContent()

    # print l
    # a = '<div class="date date--v2" data-seconds="1327328123" data-datetime="23 January 2012">23 January 2012</div>'
    # result = re.search(r'date\sdate--v\d',a)
    # print result.group()
    # a ='<div class="date date--v2" data-seconds="1327328123" data-datetime="23 January 2012">23 January 2012</div><div class="date date--v1" data-seconds="1327328123" data-datetime="23 January 2012">23 January 2012</div>'
    # soup = BeautifulSoup(a)
    # b = soup.find_all(name='div',attrs={'class':re.compile(r'date\sdate--v\d')})
    # print b