#!/usr/bin/env python
#coding:utf-8
'''
Created on 2016年1月9日

@author:yang.hongsheng 
'''

import cPickle 
import redis
import time
import win32con
import win32clipboard as w
import logging
import sys,os
import hashlib
import threading
import datetime
import codecs
import json
from pytz import timezone
from multiprocessing import Queue

ip ="waps-20"
password = "www.wasu.com"
time_out = 60
local_thread = threading.local()
file_path = "E:\\robbot\\"

expire = 1296000
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


def getText():
    try:
        w.OpenClipboard()
        d = w.GetClipboardData(win32con.CF_TEXT)
        w.CloseClipboard()
    
        return d
    except:
        setText("done")
        return "done"
    
def setText(aString):
    try:
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_TEXT, aString)
        w.CloseClipboard()
    except:
        print "OpenClipboard have issue."

    
    
def open_file(filename):
    if os.path.exists(filename):
        try:
            #myfile = codecs.open(filename, 'r',encoding = 'utf-16-le')
            myfile = codecs.open(filename, 'r',encoding = 'utf-8')
            return myfile
        except:
            print "open file error "
            return False
    else:
        print "File no exists"
        return False

def user_cmd(username,key):
    r = username + ":" +key
    return r 

def user_get(username):
    a = [user_cmd(username, "cmds"),user_cmd(username, "status")]
    return a


def set_to_redis_more(mhash,res):
    
    try:

        key2 = mhash +":res" 
        keytime = mhash + ":time" 
        key3 =mhash +":status"
        #res_redis=""           
        myredis.set(keytime,time.ctime(),ex=expire)
        myredis.set(key3,"done",ex=expire)
        #for i in res:
        #    res_redis = res_redis + i + "**"
        #myredis.set(key2,res_redis,ex=expire)
        myredis.set(key2,res,ex=expire)
        msg = "   Commands:  Hash: %s  Status: %s " % (mhash,"Done")
        logging.info(msg)
        return True
    except:
        msg = "  Commands:  Hash: %s  Status: %s " % (mhash,"issue!")
        logging.info(msg)
        return False

 
def get_jp_time():
    filename = file_path + "status"
    n= 0
    while n <3:
        f = open_file(filename)
        n= n+1
        if f:
            f = codecs.open(filename, 'r',encoding = 'utf-16-le')
            #f = codecs.open(filename, 'r',encoding = 'utf-8')
            x = f.read().splitlines()
            f.close()
            try:
                s = x[0].strip().split()
                if len(s) == 6:
                    j = datetime.datetime(int(s[0]),int(s[1]),int(s[2]),int(s[3]),int(s[4]),int(s[5]))
                    d = datetime.datetime.now(timezone('US/Pacific'))
                    d = d.replace(tzinfo=None)
                    c = (d -j).seconds
                    return c
                    break
                else:
                    break
            except:
                time.sleep(1)
                
 #get-date -Format MM:SS | convertTo-Json
                
def thread_wait_result(mhash, wait_time =500):
    filename = file_path + mhash
    begin_time=time.time()
    while (time.time() - begin_time) < wait_time:
        time.sleep(1)
        #f = open_file(filename)
        f =open_file(filename)
        if f:
            #x = f.read().splitlines()
            x = f.read()
            print x
            set_to_redis_more(mhash,x)
            f.close()
            break
        else:
            continue
        
    else:
        sys.stdout.write("Time out!")
        sys.stdout.flush()
        msg = "  Run commands:  %s   timeout! " % (mhash)
        logging.info(msg)

myredis.set("jumpbox:status","issue")
import time
ISOTIMEFORMAT="%Y-%m-%d %X"
n=0
user_list= cPickle.loads(myredis.get("user_list"))
print user_list
while True:
    cmds =[] 
    cmds_name =[]
    time.sleep(1)
    # jumpbox and zhuji  time cha 60s
    jp_time = getText().split(":")
    myredis.set("jumpbox:time",time.strftime(ISOTIMEFORMAT, time.localtime()))
    if len(jp_time) ==3:
        try:
            jp_min = int(jp_time[1])
            local_min =int(time.localtime().tm_min)
            if local_min ==0:
                local_min = 60
            if (local_min - jp_min +1) >=0:
                if myredis.get("jumpbox:status") == "issue" :
                    myredis.set("jumpbox:status","running")
                    
                    msg = "Jumpbox Staus OK! "
                    logging.info(msg) 
                

            else:
                myredis.set("jumpbox:status","issue")
                myredis.set("jumpbox:time",time.strftime(ISOTIMEFORMAT, time.localtime()))
                msg = "Jumpbox Staus have Issue! "
                logging.info(msg)
                print msg
                continue
                
        except:
            print "Jumpbox time issue."
            continue 
    else:
        n=n+1
        if n >=60:
            myredis.set("jumpbox:status","issue")
            myredis.set("jumpbox:time",time.strftime(ISOTIMEFORMAT, time.localtime()))
            msg = "Jumpbox Staus have Issue! "
            logging.info(msg)
            print "Jumpbox time len issue or timeout!!."
        continue 
     
    for i in user_list:
        key1 = i +":cmds"
        key2 = i + ":status"
        if myredis.get(key2) =="submit":
            #cmd = res[0].strip().strip(';')
            user_cmd = cPickle.loads(myredis.get(key1))
            cmds.extend(user_cmd)
            cmds_name.append(i)
            msg = "  username: %s  commands: %s" % (i,user_cmd)
            logging.info(msg)
            print msg
            
    #print cmds,cmds_name
    mhash=[]
    for i in cmds:
        mhash.append(i["name"]) 
        
    for i in mhash:
        filename =file_path + i
        try:
            os.remove(filename)
        except:
            print "Not found this file"
             
    if cmds  and "done" in getText():
        setText(json.dumps(cmds))
        for i in cmds_name:
            key2 =  i + ":status"
            myredis.set(key2,"done",ex=expire)
            
        msg = "  Run commands: %s" % cmds
        logging.info(msg)
    else:
        msg = "  Commands None or Powershell run other command, need wait" 
        logging.info(msg)
        time.sleep(1) 
        print msg
        continue  


        
    threads = []
    n=0   
    print mhash

            
    for hs in mhash:    
        
        t = threading.Thread(target=thread_wait_result,args=(hs,))
        threads.append(t)
    


    for t in threads:
        t.setDaemon(True)
        t.start()
    
    # wait the thread over
    #for t in threads:
    #    t.join()

    print "--------------Done---------------"
            

myredis.set("jumpbox:status","issue")
myredis.bgrewriteaof()

print "RUn over!"        

