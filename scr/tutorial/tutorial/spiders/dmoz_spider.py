# -*- coding: utf-8 -*-
__author__ = 'yinzishao'

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from ..items import DmozItem                 #引用问题   (..)
class DmozSpider(BaseSpider):
    name = "dmoz"
    allowed_domains =["dmoz.rog"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self,response):
        # filename = response.url.split("/")[-2]
        # open(filename,'wb').write(response.body)
        items = []

        hxs = HtmlXPathSelector(response)
        sites = hxs.xpath('//fieldset/ul/li')
        for site in sites:
            item = DmozItem()
            item['title'] = site.xpath('a/text()').extract()
            # print item['title']
            item['link'] = site.xpath('a/@href').extract()
            item['desc'] = site.xpath('text()').extract()
            items.append(item)
        return items