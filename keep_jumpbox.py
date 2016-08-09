#!/usr/bin/env python
#coding:utf-8

import pyautogui
import time,sys
import signal
from win32api import GetSystemMetrics
import random
import redis
import os
import logging
from multiprocessing import Queue
ip ="waps-20"
password = "******"
time_out = 60
FILE=os.getcwd()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s:%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename = os.path.join(FILE,'keep_jumpbox_log.txt'),
                    filemode='w')
try:
    myredis = redis.Redis(host=ip,password=password,port = 6379)
    print "Connect Redis OK!"
    logging.info('Connect Redis OK!')

except:
    print "Redis connect issue!"
    logging.info('Redis connect issue!')
    sys.exit()
#from testing.FC_server import *

buttons = {'mooncake':"E:\\pic\\mooncake.PNG",
           '06vip':"E:\\pic\\06vip_2.PNG",
           'login_ok':"E:\\pic\\login_OK.PNG",
           'key_no':"E:\\pic\\key_no.PNG",
           "desktop":"E:\\pic\\Jupbox_desktop.PNG",
           "password":"E:\\pic\\input_password.PNG",
           "ps":"E:\\pic\\ps.PNG",
           "on_screen":"e:\\pic\\On_screen.PNG",
           
           
           
           }

shift_keyboard = {"~":"`","!":"1","@":"2","#":"3","$":"4","%":"5","^":"6","&":"7","*":"8",
                "(":"9",")":"0","_":"-","+":"=","{":"[","}":"]","|":"\\",":":";",
                '"':"'","<":",",">":".","?":"/"
                }



def onscreen_keyboard(file_name):
    unite_x =34
    unite_y = 29
    hang =3
    lie =3
    offset_x =3 -lie
    offset_y =3
    keyboard = {}
    try:
        n=0
        while n<4:
            try:
                x,y,e,q = pyautogui.locateOnScreen(file_name,60)
                print x,y
                break
            except:
                continue
        
        keyboard['begin1']=[x+5,y-10]
        
        c =0
        line1 = ["esc","`","1","2","3","4","5","6","7","8","9","0","-","=","backspace"]
        line2 = ["tab","q","w","e","r","t","y","u","i","o","p","[","]","\\","del",]
        line3 = ["caps","a","s","d","f","g","h","j","k","l",";","'","enter"]
        line4 =["left_shift","z","x","c","v","b","n","m",",",".","/","up","right_shift"]
        line5 = ["fn","left_ctrl","windows","left_alt"," ","right_alt","right_ctrl","left","down","right","menu"]
        for j  in range(1,6):
            
            line_name = "line" +str(j)
            len_str =  len(eval(line_name)) +1
            
            for i in xrange(1,len_str):
                if j <= 4:
                    c = x + offset_x + (unite_x + lie) *i - unite_x /2 -lie +20 * (j-1)
                else:
                    c = x + offset_x + (unite_x + lie) *i - unite_x /2 -lie
                    
                d = y +  offset_y + (unite_y +hang)*j- unite_y /2 -hang
                
                if j==5 and i >=5 :
                    c = c+ 209 - unite_x
                pyautogui.moveTo(c,d,0.5)
                keyboard[eval(line_name)[i-1]]=[c,d]
            
    except Exception, e:
        msg = "onscreen_keyboard funcation:" + e
        print  time.ctime(),msg 
        logging.info(msg)
        keyboard ={}
        
            
    return keyboard
'''
def get_keyboard(file_name):
    unite_x =35
    unite_y = 34
    hang =4
    lie =4
    offset_x =3 -lie
    offset_y =3
    keyboard = {}
    try:
        x,y,e,q = pyautogui.locateOnScreen(file_name,60)
        print x,y
        c =0

        line1 = ["esc","`","1","2","3","4","5","6","7","8","9","0","-","=","backspace"]
        line2 = ["tab","q","w","e","r","t","y","u","i","o","p","[","]","\\","del",]
        line3 = ["caps","a","s","d","f","g","h","j","k","l",";","'","enter"]
        line4 =["left_shift","z","x","c","v","b","n","m",",",".","/","up","right_shift"]
        line5 = ["fn","left_ctrl","windows","left_alt"," ","right_alt","right_ctrl","left","down","right","menu"]
        for j  in range(1,6):
            
            line_name = "line" +str(j)
            len_str =  len(eval(line_name)) +1
            
            for i in xrange(1,len_str):
                if j <= 4:
                    c = x + offset_x + (unite_x + lie) *i - unite_x /2 -lie +20 * (j-1)
                else:
                    c = x + offset_x + (unite_x + lie) *i - unite_x /2 -lie
                    
                d = y +  offset_y + (unite_y +hang)*j- unite_y /2 -hang
                
                if j==5 and i >=5 :
                    c = c+ 209 - unite_x
                
                keyboard[eval(line_name)[i-1]]=[c,d]
            
    except Exception,e:
        print e
        msg = "get_keyboard funcation:" + e
        print  time.ctime(),msg 
        logging.info(msg)
        keyboard ={}
        
            
    return keyboard
'''
def find_image(image_file, timeout = 60):
    x =0
    y =0
    try:
        x,y,c,d = pyautogui.locateOnScreen(image_file,timeout)
        if x  and y :
            x= x + c /2
            y = y + d /2
        else:
            x =0
            y =0
            
        return x,y
    except:
        return x,y

def click_image(image_file):
    x=0
    y=0
    x,y = find_image(image_file)
    if x and y:
        pyautogui.doubleClick(x,y)
        time.sleep(2)
    else:
        S = "Can not found %s !" % image_file
        print S
        S =S + "software will exit."
        pyautogui.alert(S, 'Alert')
        sys.exit()

def onscreen_keyboard_input(keyboard,input_str,sleep_time =0.5):
    try:
        pyautogui.moveTo(keyboard_in["begin1"])  
        for i in list(input_str):
            
            if keyboard.has_key(i):
                pyautogui.click(keyboard[i])
                time.sleep(sleep_time)
            elif i.isupper():
                i = i.lower()
                if keyboard.has_key(i):
                    #pyautogui.click(keyboard_in["begin1"])
                    pyautogui.click(keyboard["left_shift"])
                    #pyautogui.click(keyboard_in["begin1"])
                    pyautogui.click(keyboard[i])
                    #pyautogui.click(keyboard_in["begin1"])
                    time.sleep(sleep_time)
            else:
                #pyautogui.click(keyboard_in["begin1"])
                pyautogui.click(keyboard["left_shift"])
                #pyautogui.click(keyboard_in["begin1"])
                pyautogui.click(keyboard[shift_keyboard[i]])
                #pyautogui.click(keyboard_in["begin1"])
                time.sleep(sleep_time)
          
    #except:
    except Exception,e:  
        print("have issue. exit input string")
        msg = "onscreen_keyboard_input  funcation:" + e
        print  time.ctime(),msg 
        logging.info(msg)
        #sys.exit(1)


    #pyautogui.typewrite(password, interval=0.5) 
    #pyautogui.press('enter')

def close_rdp():
    file_name ="e:\\pic\\disconnect.PNG"
    
    x,y = find_image(file_name, timeout=10)
    print x,y

    if x and y:
    
    
        x=GetSystemMetrics(0) -80
        y=11
        print x,y
        pyautogui.click(x, y)
    else:
        print "Not disconnect!"

def move_mouse():
    x = random.randrange(0,GetSystemMetrics(0))
    y = random.randrange(0,GetSystemMetrics(1))
    pyautogui.moveTo(x, y, 1)
    
ISOTIMEFORMAT="%Y-%m-%d %X"

myredis.set("keepjumpbox:time",time.strftime(ISOTIMEFORMAT, time.localtime()))

if __name__== '__main__':
    pyautogui.FAILSAFE = False # disables the fail-safe

    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, onscreen_keyboard_input)
  
    #fc_server_main()
    print "--------------------Keep the rdp working-------------------------------"
    
    name = "This Wasu RDtool Web Server! Please do not touch!"
    n = 0
    #while True:
    while 1:
        time.sleep(3)
        #move_mouse()
        n=n+1
        myredis.set("keepjumpbox:time",time.strftime(ISOTIMEFORMAT, time.localtime()))
        keyboard_in=onscreen_keyboard(buttons['on_screen'])
        if keyboard_in:
            onscreen_keyboard_input(keyboard_in,name,sleep_time =1)
            try:
                pyautogui.click(keyboard_in["enter"])
                time.sleep(1)
                pyautogui.moveTo(keyboard_in["begin1"])
                print n,name
                logging.info(name)
            
            except Exception,e:  
                print Exception,":",e
                print " click enter have issue. waiting response"
                logging.info(e)
            #break
           
        else:
            #check_windows_lock()
            close_rdp()
            logging.info("sys exit")
            break
        
    
        print "---------OK-----------"
