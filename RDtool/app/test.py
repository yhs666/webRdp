#!/usr/bin/env python
#coding:utf-8
'''
Created on Apr 2, 2016

@author: yang.hongsheng
'''
DATABASES = {
 
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
     
        'NAME': 'wasu',
        'USER':'wasu%mysql',
        'PASSWORD': 'hongsheng1@',
        'HOST': 'wasu.mysqldb.chinacloudapi.cn',
        'PORT': 3306,
    }
             
             
}

print DATABASES['default']['USER']


import MySQLdb
 
try:
    conn=MySQLdb.connect(host='wasu.mysqldb.chinacloudapi.cn',user='wasu%mysql',passwd='hongsheng1@',db='wasu',port=3306)
    cur=conn.cursor()
    #cur.execute('select * from user')
    cur.close()
    conn.close()
    print "ok"
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])
