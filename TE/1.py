#!/usr/bin/python
#-*- coding: utf-8 -*-
#
# Create by Meibenjin.
#
# Last updated: 2013-04-02
#
# google search results crawler
import json

import sys
import urllib2, socket, time
import gzip, StringIO
import re, random, types

reload(sys)
sys.setdefaultencoding('utf-8')


from bs4 import BeautifulSoup
class SearchResult:
    def __init__(self):
        self.url= ''
        self.title = ''
        self.content = ''

    def getURL(self):
        return self.url

    def setURL(self, url):
        self.url = url

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def getContent(self):
        return self.content

    def setContent(self, content):
        self.content = content

    def printIt(self, prefix = ''):
        print 'url\t->', self.url
        print 'title\t->', self.title
        print 'content\t->', self.content
        print

    # def writeFile(self, filename):
    #     file = open(filename, 'a')
    #     try:
    #         file.write('url:' + self.url+ '\n')
    #         file.write('title:' + self.title + '\n')
    #         file.write('content:' + self.content + '\n\n')
    #
    #     except IOError, e:
    #         print 'file error:', e
    #     finally:
    #         file.close()


def a(url):
            base_url = 'https://www.google.com.hk/'
            request = urllib2.Request(url)
            # length = len(user_agents)
            # index = random.randint(0, length-1)
            # user_agent = user_agents[index]
            # print user_agent
            user_agent='Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.11) Gecko/20080126 Firefox/2.0.0.11 Flock/1.0.8'
            request.add_header('User-agent', user_agent)
            request.add_header('connection','keep-alive')
            request.add_header('Accept-Encoding', 'gzip')
            request.add_header('referer', base_url)
            response = urllib2.urlopen(request)
            html = response.read()
            # print html
            #
            # decodejson = json.loads(html)
            # results = decodejson['responseData']['results']
            #
            # for i in results:
            #
            #   print i['title'] + ": " + i['url']
            # print type(decodejson)
            if(response.headers.get('content-encoding', None) == 'gzip'):
                    html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()
            # a =json.dumps(html)
            # print a
            # decodejson = json.loads(a)
            # s = decodejson.encode('utf-8')
            # print type(decodejson.encode('utf-8'))
            # d=eval(s)
            # print type(d)
            # print decodejson
            # print html
            # print type(html)
            api = GoogleAPI()
            result = api.extractSearchResults(html)
            # print result

            for a2 in result:
                # print a2
                # pass
                # print a2
                a2.printIt()

            # print html
class GoogleAPI:
    def __init__(self):
        timeout = 40
        socket.setdefaulttimeout(timeout)

    def randomSleep(self):
        sleeptime =  random.randint(6, 12)
        time.sleep(sleeptime)

    #extract the domain of a url
    def extractDomain(self, url):
        domain = ''
        pattern = re.compile(r'http[s]?://([^/]+)/', re.U | re.M)
        url_match = pattern.search(url)
        if(url_match and url_match.lastindex > 0):
            domain = url_match.group(1)

        return domain

    #extract a url from a link
    def extractUrl(self, href):
        url = ''
        pattern = re.compile(r'(http[s]?://[^&]+)&', re.U | re.M)
        url_match = pattern.search(href)
        if(url_match and url_match.lastindex > 0):
            url = url_match.group(1)

        return url

    # extract serach results list from downloaded html file
    def extractSearchResults(self, html):
        # print html
        results = list()
        soup = BeautifulSoup(html)
        div = soup.find('div', id  = 'search')
        if (type(div) != types.NoneType):
            lis = div.findAll('li', {'class': 'g'})
            if(len(lis) > 0):
                # print len(lis)
                for li in lis:
                    result = SearchResult()
                    h3 = li.find('h3', {'class': 'r'})
                    if(type(h3) == types.NoneType):
                        continue

                    # extract domain and title from h3 object
                    link = h3.find('a')
                    if (type(link) == types.NoneType):
                        continue

                    url = link['href']
                    # print url
                    url = self.extractUrl(url)
                    if(cmp(url, '') == 0):
                        continue
                    title = link.renderContents()
                    result.setURL(url)
                    result.setTitle(title)

                    span = li.find('span', {'class': 'st'})
                    if (type(span) != types.NoneType):
                        content = span.renderContents()
                        result.setContent(content)
                    results.append(result)
        return results



if __name__ == '__main__':
    a('https://www.google.com.hk/search?q=21st-century+maritime+silk+road+site:www.reuters.com/&safe=active&hl=en&ei=iK1xVY6TKYXoUtWngJAL&start=30&sa=N&biw=1366&bih=644')

