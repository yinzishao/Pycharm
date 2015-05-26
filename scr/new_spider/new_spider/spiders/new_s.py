# -*- coding: utf-8 -*-
__author__ = 'yinzishao'

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from ..items import NewsSpiderItem                 #引用问题   (..)
class NewsSpider(BaseSpider):
    name = "news"
    allowed_domains =["huffingtonpost.com"]
    start_urls = [

        "http://www.huffingtonpost.com/search.php/?q=21st-century+maritime+silk+road"
    ]

    def parse(self,response):
        # filename = response.url.split("/")[-2]
        # open(filename,'wb').write(response.body)
        items = []

        hxs = HtmlXPathSelector(response)
        sites = hxs.xpath('//fieldset/ul/li')
        for site in sites:
            item = NewsSpiderItem()
            item['url'] = site.xpath('a/text()').extract()
            items.append(item)
        return items