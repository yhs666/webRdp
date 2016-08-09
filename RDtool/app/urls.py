#!/usr/bin/env python
#coding:utf-8
'''
Created on Mar 6, 2016

@author: yang.hongsheng
'''
from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^app/$', views.index),
    url(r'^home/$', views.home_user, name='home'),
    #etc.
    url(r'^conta', views.conta, name='conta'),
    url(r'^ajax_list/$', views.ajax_list, name='ajax-list'),
    url(r'^ajax_dict/$', views.ajax_dict, name='ajax-dict'),
    url(r'^add/$', views.add, name='add'),
    url(r'^t/$', views.t, name='t'),

]