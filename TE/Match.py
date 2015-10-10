# # __author__ = 'yinzishao'
# # # coding=utf-8
# # import re
# # m = re.match(r'<div class="para">([\u4e00-\u9fa5]+.*?)</a></div>', '<div class="para">ksjfsdf升水</a></div></a></div>')
# #
# # print m.group(1)
#
# #coding=utf-8
#
# import urllib2
# import re
# def Crawl(url):
#     html=urllib2.urlopen(url)
#     content=html.read()
#     print(type(content))
#     content=str.decode(content,'utf-8')
#     # print(content)
#     patter=re.findall(r'<div.*?class="para">(.*?)</div>',content,re.S)
#     for item in patter:
#         p = re.compile('<([\s\S]*?)>')
#         print(p.sub("",item))
#
# Crawl("http://baike.baidu.com/subview/3539/10605302.htm")

import re
text = "JGood is a handsome boy, he is cool, clever, and so on..."
m = re.search(r'\shan(ds)ome\s', text)
if m:
    print m.group(0), m.group(1)
else:
    print 'not search'
