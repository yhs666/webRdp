#coding=utf-8
from django.contrib import admin

from models import *
# Register your models here.

class admin_cmds(admin.ModelAdmin):
    #admin the db lie
    #fields = ['SiteZone','Switch','Port ','Siteinfo','SiteNo','create_time','update_time']
    list_display = ['user_name','md5_name','cmd_path','cmd','cmd_status','create_time','update_time']
    # #define search
    search_fields = ('user_name','md5_name','cmd')

    # left bar
    list_filter=('user_name','md5_name','create_time','update_time')

    #date_hierarchy = 'update_time'
    
    

class admin_cluster(admin.ModelAdmin):

    list_display = ['name','group']


class admin_RdtoolUser(admin.ModelAdmin):
    list_display = ['user','email',]

class hideModelAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return False
   

class admin_logs(admin.ModelAdmin):
    #admin the db lie
    #fields = ['SiteZone','Switch','Port ','Siteinfo','SiteNo','create_time','update_time']
    list_display = ['username','hash','cmd','submit','jumpboxrun','cmddone','cmdstatus','create_time']
    # #define search
    search_fields = ('username','hash','cmd','create_time')

    # left bar
    list_filter=('username','hash','cmd','create_time')

    date_hierarchy = 'create_time' 
    

#admin.site.register(cmds,admin_cmds)
admin.site.register(cluster,admin_cluster)
admin.site.register(logs,admin_logs)
admin.site.register(RdtoolUser,admin_RdtoolUser)
admin.site.register(Group,hideModelAdmin)
#admin.site.register(Parameter,hideModelAdmin)
admin.site.register(Parameter,)
admin.site.register(Rdtoolcmd,)
admin.site.register(cmd_Type,hideModelAdmin)

