#coding:utf-8
"""RDtool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import *
from  main import views

admin.autodiscover()

urlpatterns = [

    #url(r'^$', views.LogIn, name='home')
    url(r'^$', views.LogIn),
    url(r'^login/$', views.LogIn),
    url(r'^index/$', views.account_auth),
    url(r'^showDashboard$', views.showDashboard),
    url(r'^logout$', views.logout_view),
    url(r'^fcclient/$', views.fcclient),
    url(r'^runcommand/$', views.runcommand),
    url(r'^getresult/$', views.getresult),
    url(r'^getresult2/$', views.getresult2),
    url(r'^submit/$', views.submit),
    url(r'^history/$', views.history),
    url(r'^server_status/$', views.server_status),
    url(r'^runping/$', views.runping),
    url(r'^PsPing$', views.PsPing),
    #(?P<year>\d{4}) 
    #(?P<hash>(([a-z]|[A-Z]|[0-9]){32}))
    # url(r'^index2/$', views.index2),
    url(r'^clusters/$', views.clusters),
    url(r'^loadInfo/$', views.loadInfo),

 

]
