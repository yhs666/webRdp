#coding:utf-8
from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, render_to_response, RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Template,Context
from django.template.loader import get_template
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db import close_old_connections
from django.db import connection
from datetime import datetime
import django.db
import json
import time
import hashlib
#from models import Devinfo, Check_Devinfo, ServerStatus, DevForm
#from models import Group,IP,RemoteUser,OpsLog,OpsLogTemp,TriaquaeUser,AuthByIpAndRemoteUser,QuickLink
from models import *
from forms import *
from myredis import myredis

expire = 1296000
import cPickle
def LogIn(request):
    if request.user is not None:
        logout_view(request)
    t = get_template("login.html")
    html = t.render({Context(),})
    return HttpResponse(html)


def account_auth(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    tri_user = auth.authenticate(username=username,password=password)
    if tri_user is not None:
        auth.login(request,tri_user)
        return HttpResponseRedirect('/showDashboard')
    else:
        return render_to_response('login.html',{'login_err':'Wrong username or password!'})
#
@login_required
def showDashboard(request):
    #return render_to_response('index.html',{'user':request.user , 'quick_links': QuickLink.objects.all()})
    redis ="ok"
    def Caltime(date1):
        date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
        date1= datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
        date2 =datetime.now()
	if date2 > date1:
            return date2-date1
        else:
            return date1-date2
    
    try:
        #if Caltime(myredis.get("keepjumpbox:time")).seconds  > 300 or  Caltime(myredis.get("jumpbox:time")).seconds >60 :
        #    print "fc_server or kepp_jumpbox have stop."
        #    myredis.set("jumpbox:status","issue")
        #    jupbox="issue"
        if Caltime(myredis.get("keepjumpbox:time")).seconds  > 300:
            print "keepjumpbox time issue."
            jupbox="issue"
        elif Caltime(myredis.get("jumpbox:time")).seconds >60:
            print Caltime(myredis.get("jumpbox:time")).seconds
            print  "jumpbox time issue."
            jupbox="issue"
            
        elif myredis.get("jumpbox:status") == "running":
            jupbox ="ok"
        else:
            jupbox="issue"
    except Exception,e:
        print Exception,":",e
        redis ="issue"
        jupbox="issue"

    
    return render_to_response('index.html',{'user':request.user ,'jupbox':jupbox,"redis":redis, })

def logout_view(request):
    user = request.user
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponse("%s logged out!" % user)

@login_required
def fcclient(request):
    t = get_template('command_execution.html')
    #html=t.render(Context({'form_name':'Enter your command:'}))
    html=t.render(Context({'user':request.user,}))
    return HttpResponse(html)


'''
@login_required
def cmd_result(request):
                track_id = request.GET['TrackMark']
                total_tasks = request.GET['TotalTasks']
                success_tasks= OpsLog.objects.get(track_mark = track_id).success_num
                failed_tasks = OpsLog.objects.get(track_mark = track_id).failed_num

        command_result = OpsLogTemp.objects.filter(track_mark = track_id)
        data_dic = {}
        for ip in command_result:
            data_dic[ip.ip] = [ip.ip, ip.user,  ip.event_log,  ip.result ]

        data_dic['result_count'] = [success_tasks, failed_tasks]
            return HttpResponse(json.dumps(data_dic))
     

@login_required
def runCmd(request):
    track_mark = MultiRunCounter.AddNumber()
    user_input = request.POST['command']
    user_account = request.POST['UserName']
    iplists = request.POST['IPLists'].split(',')

    task_num = len(set(iplists))
    print "user input command is: %s and username is:%s and iplists are: %s" %(user_input,user_account,' '.join(iplists))
    cmd = "python %s/TriAquae/backend/multiprocessing_runCMD2.py %s '%s' '%s' %s &" % (tri_config.Working_dir,track_mark,' '.join(iplists),user_input,user_account)
    os.system(cmd)
    return HttpResponse('{"TrackMark":%s, "TotalNum":%s}' %(track_mark, task_num))
'''
from forms import *
''' 
def index2(request):
    if request.method == 'POST': # 如果表单被提交
        form = Fcclient(request.POST) # 获取Post表单数据
        if form.is_valid(): # 验证表单
            print form.cleaned_data['cluster']
            print form.cleaned_data['cmd']
            print form.cleaned_data['parameter']
            return HttpResponseRedirect('/') # 跳转
    else:
        form = Fcclient() #获得表单对象
                
        return render_to_response('index2.html', {
                'form': form,
        })
 '''       
        
@login_required
def clusters(request):
    data = []
    counter = 0
    group_list2  = Group.objects.all()
    for g in group_list2:
        g_name = g.name
        counter += 1
        clusterin_group = cluster.objects.filter(group__name = g_name).count()
        data.append({'id': counter, 'pid':0, 'text':'%s [%s]' %(g_name,clusterin_group), 'bgroup':1})
        cluster_list =  cluster.objects.filter(group__name = g_name)
        ip_counter = 0
        for cluster2 in cluster_list:
            ip_counter += 1
            data.append({'id':'%s%s'%(counter,ip_counter), 'pid': counter, 'text':cluster2.name,'bgroup':0 , 'ip':cluster2.name })

        '''data=[
         { 'id':1,'pid':0, 'text': 'Node 1','bgroup':1},
         { 'id':11,'pid':1, 'text': 'Node 1.1','bgroup':0},
         { 'id':12,'pid':1, 'text': 'Node 1.2','bgroup':0},
         { 'id':2,'pid':0,'text': 'Node 2' ,'bgroup':0},
         { 'id':3,'pid':0,'text': 'Node 3' ,'bgroup':0},
         { 'id':4,'pid':0,'text': 'Node 4' ,'bgroup':0},
         { 'id':5,'pid':0,'text': 'Node 5' ,'bgroup':0},
         ];'''
    #print data
    return HttpResponse(json.dumps(data))

def loadInfo(request):
    data = []
    
    #print Rdtoolcmd.objects.all()
    for cmd in Rdtoolcmd.objects.all():
        cmd_name = cmd.name
        h=cmd.help
        p=[]
        for i in cmd.param.all():
            p.append(i.name)
          
        data.append({"command":cmd_name,"param":p,"help":h})
    #print data
    
    #date  [{u'GetNodeEvents': [u'Node ID', u'Tenant ID']}, {u'GetTenantLbSetting': [u'Tenant ID']}]
    data2 ={"comments":data}
    #data ={"comments":[{"content":"很不错嘛","id":1,"nickname":"纳尼"},{"content":"哟西哟西","id":2,"nickname":"小强"}]}
    return HttpResponse(json.dumps(data2)) 

@login_required
def runcommand(request):
    username =  request.user
    cmds = request.GET["cmd"]
    cmds = json.loads(cmds)
    #cmd {u'cluster': [u'BJBprdapp01'], u'command': u'GetNodeEvents', u'param': {u'Node ID': u'ffffffff'}}
    clusters = cmds["cluster"]
    command = cmds["command"]
    param = cmds["param"]
    #  Prompte NoUseHistroy  UseHistroy
    pro = cmds['prompte']
    md5 = hashlib.md5()
    cmd_list=[]
    cmd0 ="FCClient.exe"
    run_path = "Fabric"
    pro_list=[]
    new_list=[]
    print pro
    #confirm command allow run
    if Rdtoolcmd.objects.filter(name=command):
        if len(param) ==1:
            for cluster in clusters:
                for k in param.keys():
                    v= param[k]                   
                run_cmd = cmd0 + "  c:" +cluster +"  " + command +":"+v
                #print run_cmd
                md5.update(run_cmd)
                hash0 =md5.hexdigest()
                key1 = hash0 + ":cmd"
                key2 = hash0 + ":cmdstatus"
                key3 = hash0 + ":time"
                key4 = hash0 + ":path"
                key5 = hash0 + ":exe"
                key6 = hash0 + ":status"
                if  pro !="NoUseHistroy" and myredis.exists(key1):
                    pro_list.append({"cmd":run_cmd,"hash":hash0,"status":myredis.get(key2),"time":myredis.get(key3)})
                else:
                    #myredis.mset({key1:run_cmd,key4:run_path,key5:cmd0}) 
                    myredis.set(key1,run_cmd,ex=expire)
                    myredis.set(key4,run_path,ex=expire)
                    myredis.set(key5,cmd0,ex=expire)
                    #myredis.set(key6,"submit",ex=expire)
                    new_list.append(hash0)

            cmd_list.append(pro_list)
            cmd_list.append(new_list)
            
            print cmd_list
                
        elif len(param)> 1:
            for cluster in clusters:
                run_cmd= cmd0 + "  c:" +cluster +"  " + command + "  " 
                for k in param.keys():
                    v= param[k]
                    run_cmd =run_cmd  + k +":"+ v +"  "
                md5.update(run_cmd)  
                hash0 =md5.hexdigest()
                key1 = hash0 + ":cmd"
                key2 = hash0 + ":cmdstatus"
                key3 = hash0 + ":time"
                key4 = hash0 + ":path"
                key5 = hash0 + ":exe"
                if pro !="NoUseHistroy" and myredis.exists(key1):
                    pro_list.append({"cmd":run_cmd,"hash":hash0,"status":myredis.get(key2),"time":myredis.get(key3)})
                else:
                    myredis.set(key1,run_cmd,ex=expire)
                    myredis.set(key4,run_path,ex=expire)
                    myredis.set(key5,cmd0,ex=expire)
                    new_list.append(hash0)
                
            cmd_list.append(pro_list)
            cmd_list.append(new_list)
            
        else:
            re_data="Param Error!"
            
    else:
        
        re_data = "Command not Allowed run !"
    
    if len(cmd_list) == 0:
        data2 = [{"hash":"None","cmd":command},re_data,"issue"]
        cmdlog = logs(username=username,hash="None",cmd=command,submit=re_data)
        cmdlog.save()
        return HttpResponse(json.dumps(data2))
    else:
        return HttpResponse(json.dumps(cmd_list))
        
    # to redis [{"name":hash,"cmd":"fcclient c:bjbprdapp01 gettenantlbsettings:ddddddd","path":"fcclient"}]  

@login_required
def submit(request):
    username =  str(request.user)
    hashname = json.loads(request.GET["hash"])
    cmd_list=[]
    if myredis.get("jumpbox:status") =="running" :
        for i in hashname:
            key1 = i +":cmd"
            key2 = i +":path"
            key3 = i +":id"
            key4 = i + ":status"
            cmd = myredis.get(key1)
            cmd_path = myredis.get(key2)
            cmd_dict={"name":i,"cmd":cmd,"path":cmd_path}
            cmd_list.append(cmd_dict)
            myredis.set(key4,"submit",ex=expire)
            cmdlog = logs(username=username,hash=i,cmd=cmd,submit="submit")
            cmdlog.save()
            myredis.set(key3,cmdlog.id,ex=expire)
            
            
        key1 = "%s:cmds" % username
        key2 =  "%s:status" % username 
        key3 =  "%s:time" % username
	print key2
	print myredis.get(key2)
        #myredis.mset({key1:cPickle.dumps(cmd_list),key2:"submit",key3:datetime.now()})
        i=1
        while 1:
            try:
                if myredis.get(key2)=="done": 
                    myredis.set(key1,cPickle.dumps(cmd_list),ex=expire)
                    myredis.set(key2,"submit",ex=expire)
                    myredis.set(key3,datetime.now(),ex=expire)
                    return HttpResponse("ok")
                    break
                elif not myredis.exists(key2):
                    
                    myredis.set(key1,cPickle.dumps(cmd_list),ex=expire)
                    myredis.set(key2,"submit",ex=expire)
                    myredis.set(key3,datetime.now(),ex=expire)
                    return HttpResponse("ok")
                    break
                else :
                    time.sleep(1)
                    i=i+1
                    if i == 60:
                        print "submit hash to username time out"
                        return HttpResponse("Jumpbox busy! Please retry it 5 min later!")
                        break
            except:
                myredis.set(key1,cPickle.dumps(cmd_list),ex=expire)
                myredis.set(key2,"submit",ex=expire)
                myredis.set(key3,datetime.now(),ex=expire)
                return HttpResponse("ok")
    else:
        
        return HttpResponse("Jumpbox have issue.")
    
@login_required
def getresult(request):
    username =  str(request.user)
    hashname = request.GET["hash"]
    #used for test below
    '''
    re_status=["success","failed"]
    from random import choice
    st = choice(re_status)
    key1 = "%s:cmds" % username
    cmds0 = cPickle.loads(myredis.get(key1))
    
    for i in cmds0:
        key1 = i['name'] + ":cmd"
        key2 = i['name'] + ":user"
        key3 = i['name'] + ":status" 
        key4 = i['name'] + ":cmdstatus" 
        key5 = i['name'] + ":time"
        #myredis.mset({key1:i['cmd'],key2:username,key3:"done",key4:st,key5:"201601503"})
        myredis.set(key1,i['cmd'],ex=expire)
        myredis.set(key2,username,ex=expire)
        myredis.set(key3,"done",ex=expire)
        myredis.set(key4,st,ex=expire)
        myredis.set(key5,"201601503",ex=expire)
    '''
    key2 = str(username) + ":status"
    key3 = hashname + ":status"
    key4 = hashname + ":cmdstatus"
    key6 = hashname + ":id"
    #time.sleep(15) 
    #myredis.set(key2,"done",ex=expire)
    
    try:
        hashid = int(myredis.get(key6))
        #hash_record = logs.objects.filter(username=username,hash=hashname)[0]
        hash_record = logs.objects.get(id=hashid)
        #command to jumpbox
        flg =0
        while True:
            if myredis.get("jumpbox:status") == "running" : 
                if myredis.get(key2) =="done":
                    hash_record.jumpboxrun=datetime.now()
                    hash_record.save()
                    break
                time.sleep(0.5)
            else:
                flg =1
                break
        #command run done
        while True:
            if myredis.get("jumpbox:status") == "running" :
                if myredis.get(key3) =="done":
                    hash_record.cmddone=datetime.now() #赋值给你要更新的字段
                    try:
                        hash_record.cmdstatus = myredis.get(key4)
                    except:
                        hash_record.cmdstatus = "failed"
                    hash_record.save() #保存
                    break
                time.sleep(0.5)
            else:
                flg=1
                break
        #time.sleep(10)
        if flg == 0:
            key1= hashname + ":cmd"
            key2 = hashname + ":cmdstatus"
            cmd_dict ={"hash":hashname,"cmd":myredis.get(key1),"status":myredis.get(key2)}
            return HttpResponse(json.dumps(cmd_dict))
        else:
            cmd_dict ={"hash":hashname,"cmd":"None","status":"Jumpbox had issue"}
            return HttpResponse(json.dumps(cmd_dict))

    except:
        cmd_dict ={"hash":hashname,"cmd":"None","status":"mysql connect issue"}
        return HttpResponse(json.dumps(cmd_dict))
    
    #cmd_dict ={"hash":"hashname","cmd":"None","status":"success"}
    #return HttpResponse(json.dumps(cmd_dict))

#from django.utils.safestring import SafeString
def getresult2(request): 
    hashname =request.GET.get('hash')
    print hashname
    key = hashname + ":res"
    if myredis.exists(key):
        res = myredis.get(key)
    else:
        res=["None"]
        
    #print res
    key0 = hashname + ":cmd"
    key1 = hashname +":time"
    #return render_to_response("result.html", {"res":res,})
    return render(request,"result.html",{
                                         "res":json.dumps(res),
                                         "cmd":json.dumps(myredis.get(key0)),
                                         "time":json.dumps(myredis.get(key1)),
                                         })

@login_required
def history(request):
    username =  str(request.user)
    userlog  = logs.objects.filter(username=username).values_list()[0:100]
    return  render_to_response('history.html',{'log':userlog,})

def server_status(request):
    
    return HttpResponseRedirect('/showDashboard')

@login_required
def PsPing(request):
    
    #return  HttpResponse("OK")
    return render_to_response('ping.html',{'user':request.user, })

@login_required
def TcPing(request):
    
    return render_to_response('ping.html',{'user':request.user, })

   
@login_required
def runping(request):
    username =  str(request.user)
    cmds = json.loads(request.GET["cmd"])
    print cmds
    #cmd {u'cluster': [u'BJBprdapp01'], u'command': u'GetNodeEvents', u'param': {u'Node ID': u'ffffffff'}}
    pingname = cmds["pingname"]
    pingn = str(cmds["pingn"])
    port = str(cmds["port"])
    pro = cmds['prompte']
    md5 = hashlib.md5()
    cmd_list=[]
    cmd0 ="psping.exe"
    run_path = "PSTools"
    pro_list=[]
    new_list=[]   
    run_cmd = cmd0 + "  -n  " + pingn +"    " +  pingname + ":" + port
    #print run_cmd
    md5.update(run_cmd)
    hash0 =md5.hexdigest()
    key1 = hash0 + ":cmd"
    key2 = hash0 + ":cmdstatus"
    key3 = hash0 + ":time"
    key4 = hash0 + ":path"
    key5 = hash0 + ":exe"
    key6 = hash0 + ":status"
    if  pro !="NoUseHistroy" and myredis.exists(key1):
        pro_list.append({"cmd":run_cmd,"hash":hash0,"status":myredis.get(key2),"time":myredis.get(key3)})
    else:
        #myredis.mset({key1:run_cmd,key4:run_path,key5:cmd0})
        myredis.set(key1,run_cmd,ex=expire)
        myredis.set(key4,run_path,ex=expire)
        myredis.set(key5,cmd0,ex=expire)
        #myredis.set(key6,"submit",ex=expire) 
        new_list.append(hash0)

    cmd_list.append(pro_list)
    cmd_list.append(new_list)
    
    print cmd_list
                

    return HttpResponse(json.dumps(cmd_list))  
    
