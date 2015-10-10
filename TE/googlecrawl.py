# -*- coding: utf-8 -*-

__author__ = 'yinzishao'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2, socket, time
import gzip, StringIO
import re, random, types

from bs4 import BeautifulSoup

base_url = 'https://www.google.com.hk/'
results_per_page = 10

user_agents = list()
def a(url):
            request = urllib2.Request(url)
            # length = len(user_agents)
            # index = random.randint(0, length-1)
            # user_agent = user_agents[index]
            # print user_agent
            user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.2; en-GB; rv:1.8.1.2pre) Gecko/20070226 BonEcho/2.0.0.2pre'
            request.add_header('User-agent', user_agent)
            request.add_header('connection','keep-alive')
            request.add_header('Accept-Encoding', 'gzip')
            request.add_header('referer', base_url)
            response = urllib2.urlopen(request)
            html = response.read()
            print html
            if(response.headers.get('content-encoding', None) == 'gzip'):
                html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()

a('https://www.google.com.hk//search?hl=en&num=10&start=20&q=21st-century%20maritime%20silk%20road%20site%3Awww.economist.com')
