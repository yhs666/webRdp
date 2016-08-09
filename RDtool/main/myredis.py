#!/usr/bin/env python
#coding:utf-8
'''
Created on 2016年5月6日

@author: yang
'''
import logging
import os
import sys
import redis
ip ="192.168.56.1"
password = "www.wasu.com"
time_out = 60
FILE=os.getcwd()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename = os.path.join(FILE,'log.txt'),
                    filemode='w')
try:
    myredis = redis.Redis(host=ip,password=password,port = 6379)
    print "Connect Redis OK!"
    logging.info('Connect Redis OK!')

except:
    print "Redis connect issue!"
    logging.info('Redis connect issue!')
    sys.exit()
