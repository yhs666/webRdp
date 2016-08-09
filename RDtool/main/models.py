#coding=utf-8
from django.db import models
from datetime  import datetime

from django import forms
from django.contrib.auth.models import User
 #datetime.date.today()
'''
# Create your models here.
class Portmap(models.Model):
    SiteZone = models.CharField(max_length=10,unique=False,verbose_name = '工位区域')
    Switch = models.IPAddressField(verbose_name = '交换机IP',default = '192.168.64.1')
    Port = models.CharField(max_length=20,unique=False,verbose_name = '交换机端口')
    Siteinfo = models.CharField(max_length=10,unique=True,verbose_name = '工位信息点',help_text ='工位下面网络信息点的编号如:D137-D2')
    SiteNo = models.CharField(max_length=10,unique=False,verbose_name = '座位号')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name = '创建时间')
    update_time = models.DateTimeField(default=datetime.now(),auto_now = True,verbose_name = '修改时间')

    def __unicode__(self):
        return  self.SiteNo
    class Meta:
        db_table = 'serverinfo_portmap'#数据库名
        verbose_name='端口对应表'#修改从管理级'产品中心'进入后的页面显示，显示为'产品'
        verbose_name_plural='网络端口工位对应表'#修改管理级页面显示


class Search_history(models.Model):
    swip = models.IPAddressField()
    hostip = models.IPAddressField()
    mac = models.CharField(max_length=15)
    port = models.CharField(max_length=20)
    siteno = models.CharField(max_length=10)
    create_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return  self.hostip


#服务器对应交换机端口
class  Server_links(models.Model):
    rack =models.CharField(max_length=10,unique=True,verbose_name = '机柜编号',default='Z00')
    line_lable = models.CharField(max_length=15,unique=True,verbose_name = '网线标签')
    port = models.CharField(max_length=15,verbose_name = '交换机端口')
    swip = models.CharField(max_length=15,verbose_name = '交换机IP')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name = '创建时间')
    update_time = models.DateTimeField(default=datetime.now(),auto_now = True,verbose_name = '修改时间')

    def __unicode__(self):
        return  self.rack



#服务器信息表
class Server(models.Model):
    Status = models.CharField(max_length=30,unique=False,verbose_name = '状态信息')
    Rack = models.ForeignKey(Server_links,verbose_name='机柜编号')
    #Rack =models.CharField(max_length=10,unique=True,verbose_name='机柜编号')
    Type = models.CharField(max_length=15,unique=False,verbose_name = '服务器架构')
    Ip = models.IPAddressField(unique=True)
    Otherip = models.CharField(unique=False,max_length=40,verbose_name = '管理ip')
    Model = models.CharField(max_length=40,verbose_name = '服务器型号')
    Sn = models.CharField(max_length=20,verbose_name = '序列号')
    Tn = models.CharField(unique=False,max_length=20,verbose_name = '小型号')
    Os = models.CharField(max_length=20,verbose_name = '操作系统')
    Hostname = models.CharField(max_length=35,verbose_name = '主机名')
    Dept = models.CharField(max_length=50,verbose_name = '所属团队')
    User = models.CharField(max_length=50,verbose_name = '所属团队联系人')
    Cpu= models.CharField(max_length=40,verbose_name = '处理器')
    Ram =models.CharField(max_length=10,verbose_name = '内存')
    Disk= models.CharField(max_length=25,verbose_name = '硬盘')
    Purchase_Date = models.DateField(verbose_name = '购买日期')
    Endwarranty_Date = models.DateField(verbose_name = '保修结束日期')
    Warranty_status = models.CharField(max_length=30,verbose_name = '保修状态')
    Password = models.CharField(max_length=50,verbose_name = '服务器密码')
    Remask1 = models.CharField(unique=False,max_length=10,verbose_name = '备注1')
    Remask2 = models.CharField(unique=False,max_length=10,verbose_name = '备注2')
    Remask3 = models.CharField(unique=False,max_length=10,verbose_name = '备注3')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name = '创建时间')
    update_time = models.DateTimeField(default=datetime.now(),auto_now = True,verbose_name = '修改时间')

    def __unicode__(self):
        return  self.Ip

    class Meta:
        db_table = 'serverinfo_server'
        verbose_name='服务器信息表'
        verbose_name_plural='服务器信息表'
'''

class cmds(models.Model):
    user_name = models.CharField(max_length=20,unique=False,verbose_name = 'User name')
    md5_name = models.CharField(max_length=32,unique=False,verbose_name = 'MD5 name')
    cmd_path = models.CharField(max_length=32,unique=False,verbose_name = 'Command Path')
    #Switch = models.IPAddressField(verbose_name = '交换机IP',default = '192.168.64.1')
    cmd = models.CharField(max_length=256,unique=False,verbose_name = 'Command run')
    cmd_status = models.CharField(max_length=20,unique=False,verbose_name = 'Command status')
    #Siteinfo = models.CharField(max_length=10,unique=True,verbose_name = '工位信息点',help_text ='工位下面网络信息点的编号如:D137-D2')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name = 'Create time')
    #update_time = models.DateTimeField(default=datetime.now(),verbose_name = 'update time')

    def __unicode__(self):
        return  self.md5_name
    class Meta:
        db_table = 'Commands'#数据库名
        verbose_name='Commands run'#修改从管理级'产品中心'进入后的页面显示，显示为'产品'
        verbose_name_plural='Commands run'#修改管理级页面显示




class Group(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __unicode__(self):
        return self.name

class cluster(models.Model):
    name=models.CharField(max_length=50, unique=True)
    #ip = models.IPAddressField(unique=True)
    group = models.ForeignKey(Group, null=True, blank=True,unique=False)
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]


class RdtoolUser(models.Model):
    user = models.ForeignKey(User, null=True)
    email = models.EmailField()
    group = models.ManyToManyField(Group)
    def __unicode__(self):
        return '%s' % self.user

class Parameter(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __unicode__(self):
        return self.name

class cmd_Type(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __unicode__(self):
        return self.name 
      
class Rdtoolcmd(models.Model):
    cmds_type = models.ForeignKey(cmd_Type)
    name = models.CharField(max_length=50,unique=True)
    param = models.ManyToManyField(Parameter)
    #help = models.CharField(max_length=256,unique=False)
    help = models.TextField(blank=True,null=True)
    def __unicode__(self):
        return '%s' % self.name
    

class logs(models.Model):
    username = models.CharField(max_length=20,unique=False,verbose_name = 'User name')
    hash = models.CharField(max_length=32,unique=False,verbose_name = 'MD5 name')
    #Switch = models.IPAddressField(verbose_name = '交换机IP',default = '192.168.64.1')
    cmd = models.CharField(max_length=256,unique=False,verbose_name = 'Command run')
    submit = models.CharField(max_length=50,unique=False,verbose_name = 'submit command')
    jumpboxrun = models.DateTimeField(null=True,unique=False,blank=True,verbose_name = 'Run in Jumpbox')
    cmddone=models.DateTimeField(null=True,unique=False,blank=True,verbose_name = 'cmd done')
    cmdstatus=models.CharField(null=True,max_length=50,blank=True,unique=False,verbose_name = 'cmd done status')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name = 'Create time')
    #Siteinfo = models.CharField(max_length=10,unique=True,verbose_name = '工位信息点',help_text ='工位下面网络信息点的编号如:D137-D2')


    def __unicode__(self):
        return  self.hash
    class Meta:
        ordering = ["-create_time"]
        db_table = 'Commands logs'#数据库名
        verbose_name='Commands logs'#修改从管理级'产品中心'进入后的页面显示，显示为'产品'
        verbose_name_plural='Commands logs'#修改管理级页面显示
