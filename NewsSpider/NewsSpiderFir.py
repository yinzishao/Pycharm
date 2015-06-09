#coding=utf-8
from NewsSpider import ConnectedSQL

__author__ = 'yinzishao'

import urllib2
import re
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
TOTALNUM=0

# #根据输入的页数爬取其对应链接爬取
# def getallurl():
#     allurl =set()
#     urltemp =set()
#     for i in range(10):
#         urltemp=urlspider(i*10)
#         if urltemp==[]:       #爬不到链接断开
#             break
#         else:
#             allurl = allurl | urltemp
#
#     #写入文档
#     urlpath ='SouthChinasilkurl.txt'
#     with open(urlpath,'w') as f:
#         for i in allurl:
#             f.write(i+'\n')

#爬取页数为snum的数量

#根据keyword 搜索,并且保存在path中
def urlspider(keyword,urlpath ='SouthChinasilkurl1.txt'):
    allset= set()
    keyword=re.sub(' ','%20',keyword)
    for num in range(10):
        url ='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=10&num=10&hl=en&prettyPrint=false&sou'\
             +'rce=gcsc&gss=.com&sig=cb6ef4de1f03dde8c26c6d526f8a1f35&start='+str(10*num)+\
             '&cx=004830092955692134028:an6per91wyc&q='+keyword\
             +'&as_sitesearch=huffingtonpost.com&googlehost=www.google.com'
        urlset=geturl(url)
        if urlset==[]:       #爬不到链接断开
            break
        else:
            allset = allset | urlset

    print allset

    # while  num<int(TOTALNUM):
    #     url ='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=10&num=10&hl=en&prettyPrint=false&sou'\
    #      +'rce=gcsc&gss=.com&sig=cb6ef4de1f03dde8c26c6d526f8a1f35&start='+str(num)+\
    #      '&cx=004830092955692134028:an6per91wyc&q='+keyword\
    #      +'&as_sitesearch=huffingtonpost.com&googlehost=www.google.com'
    #     print url
    #     a,TOTALNUM =geturl(url)
    #     urlset = urlset|a
    #     num =num+10
    #     print TOTALNUM
    #     print len(urlset)
    # url='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwS'\
    #          +'G1gunmMikTzQqY&rsz=10&num=10&hl=en&prettyPrint=false&source=gcsc&gss=.com&sig=cb6ef4d'\
    #          +'e1f03dde8c26c6d526f8a1f35&start='+str(starnum)+'&cx=004830092955692134028:an6per91wyc&q=21st-century%'\
    #          +'20maritime%20silk%20road&as_sitesearch=huffingtonpost.com&googlehost=www.google.com'

    #
    with open(urlpath,'w') as f:
        for i in allset:
            f.write(i+'\n')
    print len(allset)
    return allset

#搜索得到链接
def geturl(url):
    try:
        response = urllib2.urlopen(url)
    except Exception,e:
        print e
    html = response.read()
    a=r'"url":"([^"]*?.html)"'
    b =r',"estimatedResultCount":"(\d*)",'
    a=re.compile(a)
    b =re.compile(b)
    result = re.findall(a,html)
    num = re.search(b,html).group(1)         #得到结果num


    # print result
    return set(result)


# allurl =urlspider('21st-century maritime silk road')
    #写入文档

#按行读取文档的内容并且爬内容
def readurl(path='SouthChinasilkurl.txt'):
    i=1
    for line in open(path):
        crawlcontent(line.strip(),i)
        i+=1


#爬取链接里面的内容
def crawlcontent(url,i=1):
    retry=3
    while retry>0:
            try:
                response = urllib2.urlopen(url)
                html =response.read()
                # print html
                soup  = BeautifulSoup(html)
                title =soup.find('h1',class_='title')
                title = str(title.get_text())
                time =str(soup.find('span',class_='updated').time.get_text()).strip()
                print time
                author = str(soup.find('span',class_='name fn').get_text()).strip()
                # name =re.sub('&nbsp;','',name)
                print author
                rename1 = re.compile(r'By\s*(.*)')
                # rename2 = re.compile(r'')
                res =re.search(rename1,author)        #例外:如果符合一些不规范的作者需要另外提取
                if res:
                    author=str(res.group(1)).strip()
                    print author
                # print re.sub(r'By\s*()',' ',name)
                content =soup.find('div',id='mainentrycontent')
                contenttemp =[]
                for a in content.find_all(['h1','h2','li','p','h3','h4'],attrs={'style':None}):
                    # print a
                    if a.p:
                        pass
                        # print a.get_text()
                    else:
                        # print a.get_text()
                        content =a.get_text()
                        content =re.sub('\n',' ',content)
                        contenttemp.append(content)
                # w.write(content)
                content =''.join(contenttemp)              #得到内容
                l=[url,title,author,time,content]
                #连接数据库并且提交数据
                ConnectedSQL.commit_data(l)
                break
            except urllib2.URLError,e:
                print 'url error:', e
                retry = retry - 1

                continue
            except Exception, e:
                print 'error:', e
                retry = retry - 1
                # self.randomSleep()
                continue

                # print g.ul.get_text()
                # r=re.compile(r'<div.*(\\div>)?')
                # content =re.sub(r,' ',str(content))
                # print content
                # print p


    # with open('text1.txt','a')as w:
    #
    #     w.write(str(i)+'.\n')
    #     w.write('url:'+url+'\n')
    #     w.write('title:'+title+'\n')
    #     w.write('author:'+name+'\n')
    #     w.write('time:'+time+'\n')
    #     w.write('content:')
    #     contenttemp =[]
    #     for a in content.find_all(['h1','h2','li','p','h3','h4'],attrs={'style':None}):
    #         # print a
    #         if a.p:
    #             pass
    #             # print a.get_text()
    #         else:
    #             # print a.get_text()
    #             content =a.get_text()
    #             content =re.sub('\n',' ',content)
    #             contenttemp.append(content)
    #             # w.write(content)
    #     content =''.join(contenttemp)
    #     w.write(content)
        # for a in content.find_all(name ='p',attrs={'style':'disp','type':None}):

            # print


# crawlcontent('http://www.huffingtonpost.com/kevin-rudd/us-china-relations-kevin-rudd-report_b_7096784.html')
readurl('SouthChinasilkurl1.txt')

# urlspider('silk road economic belt','SouthChinasilkurl3.txt')

# getallurl()
# print len(urlspider(0)|urlspider(10))


