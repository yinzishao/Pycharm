#coding=utf-8
import re
import ConnectedSQL
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
__author__ = 'yinzishao'

def process_retuer_url():
#     s = set()
#     with open('silk_retuer.txt','r') as r:
#         for a in r:
#             # print type(a)
#             s.add(a.strip())
#     print len(s)
    with open('silkroadurl_retuer.txt','r')as w:
        i = 0
        while(w.readline()):
            i+=1
        print i


def contenttosql(path):
    with open(path,'r')as r :
        line = r.readline()
        wrongnum =0
        num =1
        linenum=1
        # linenum+=1
        # url =line[linenum]

        while(line):
            # print line
            url =r.readline()
            title =r.readline()
            try:
                int(title)
                # print num
                num+=1
                wrongnum+=1
                # line = r.readline()
                # break

            except Exception,e:
                time = r.readline()
                content = r.readline()
                author = r.readline()
                num+=1
                line =r.readline()
                # linenum+=6
                l =[url,title,author,time,content]
                # l=[url,title,author,time,content]
                #连接数据库并且提交数据
                ConnectedSQL.commit_data(l)
                print l
                continue

            # time = r.readline()
            # content = r.readline()
            # author = r.readline()
            # num+=1
            # line =r.readline()
            # # linenum+=6
            # l =[url,title,author,time,content]
            # print l

if __name__ == '__main__':
    # with open('retuer_conment2.txt','r')as r :
    #     a =r.readlines()

    contenttosql('retuer_conment2.txt')