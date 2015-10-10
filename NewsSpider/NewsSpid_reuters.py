#coding=utf-8
__author__ = 'yinzishao'

import urllib
import urllib2
from tool import *
import re
from bs4 import BeautifulSoup
import sys
import ConnectedSQL
reload(sys)
sys.setdefaultencoding('utf-8')
surl = 'http://www.reuters.com/search/news?blob='
TOTALNUM=0


#输入关键词得到链接
def search(keyword,path='reuters.txt'):
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

    with open(path,'w')as r:
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
#按照url title  time content author格式写进文档

def crawlcontent(url,w,i=1):
    retry =3
    while retry>0:
        try:
            response = urllib2.urlopen(url)
            html =response.read()
            print str(i)+'\n'
            # w.write(str(i)+'\n')

            soup  = BeautifulSoup(html)
            w.write(url+'\n')
            title =str(soup.find('h1',class_='article-headline').get_text())
            print title
            w.write(title+'\n')
            time = str(soup.find('span',class_='timestamp').get_text())
            print time
            w.write(time+'\n')

            content = soup.find('span',id='articleText')
            content= str(content.get_text())
            # re.compile('\n')
            content =re.sub('\n',' ',content)
            print content
            w.write(content+'\n')
            r = re.compile(r'\((((W|w)riting)|((e|E)diting)|((R|r)eporting)).*?(b|B)y (.*?)(;|\))')

            # r = re.compile(r'\((Writing)|(Editing)|(Reporting).*?(b|B)y (.*?)(;|\))')
            try:
                author =re.search(r,content).group(9)
                print author
            except Exception,e:
                print e
                author =None
            w.write(str(author)+'\n')
            l=[url,title,author,time,content]
            #连接数据库并且提交数据
            # ConnectedSQL.commit_data(l)


            break
        except AttributeError,e:
            print 'AttributeError:',e
            break
        except urllib2.URLError,e:
            print 'url error:', e
            retry = retry - 1

            continue
        except Exception, e:
            print 'error:', type(e)
            retry = retry - 1
            # self.randomSleep()
            continue

def readurl(wpath,path='silkroadurl_retuer.txt'):
    with open(wpath,'w') as w:
        i=1
        for line in open(path):
            crawlcontent(line.strip(),w,i)
            i+=1

# readurl()
# crawlcontent('http://www.reuters.com/article/idUSFit91970120150415')
# search('21st-century maritime silk road')
#读取链接文档后将内容写进path中


#输入关键字以及保存链接的路径
if __name__ == '__main__':
    # keyword = ''
    # path = ''
    # search(keyword,path)
    readurl('retuer111111.txt')
