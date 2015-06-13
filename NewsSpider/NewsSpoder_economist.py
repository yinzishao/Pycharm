__author__ = 'yinzishao'

import googleapi

def get_url(keywoed):
    api  = googleapi.GoogleAPI()
    a = api.searchall(keywoed)
    # api.a()
    url_set = set()
    for s in a :
        # print type(s)
        url_set.add(s.getURL())
    print len(url_set)
    return url_set
if __name__ =='__main__':

    set1 =get_url('21st-century maritime silk road site:www.economist.com/news')
    set2 =get_url('silk road economic belt site:www.economist.com/news')
    url_all =set1|set2
    print len(url_all)
    with open('ecnomist.txt','w') as w:
        for url in url_all:
            w.write(url+'\n')
