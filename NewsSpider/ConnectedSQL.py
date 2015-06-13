#coding=utf-8
import sys
import MySQLdb
user='root'
pwd='2015'
host='192.168.235.65'
post=3306
def __init__(self):
    pass
def commit_data(l):
       url=l[0]
       title=l[1]
       author=l[2]
       time=l[3]
       main_body=l[4]
       global user
       global pwd
       global host
       global post
       try:
          conn=MySQLdb.connect(host=host,port=post,user=user,passwd=pwd,db='silk_road',charset="utf8")
       except Exception,e:
           print e
           sys.exit()
       cur=conn.cursor()
       try:
           cur.execute('insert into news(New_url,Title,Author,Time,Mb) values (%s,%s,%s,%s,%s)',(url,title,author,time,main_body))
           conn.commit()
       except Exception,e:
           print e
           conn.rollback()
       cur.close()


def search_data(url):
    global user
    global pwd
    global host
    global post
    try:
        conn=MySQLdb.connect(host=host,port=post,user=user,password=pwd,database='silk_road',use_unicode=True)
    except Exception,e:
        print(e)
        sys.exit()
    cur=conn.cursor()
    values=[]
    try:
        cur.excute('select * from use where url=%s',[url])
        values=cur.fetchall()
    except Exception,e:
        print (e)
    cur.close()
    conn.close()
    return list(values)

def update_data(url):
    global user
    global pwd
    global host
    global post
    conn=MySQLdb.connect(host=host,port=post,user=user,password=pwd,database='silk_road',use_unicode=True)
    cur=conn.cursor()
    sql='update news set....'
    cur.excute(sql)
    conn.commit()
    cur.close()
    conn.close()






