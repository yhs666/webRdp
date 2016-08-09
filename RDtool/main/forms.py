#coding:utf-8
from django import forms
from django.forms import ModelForm
from models import *
from django.template.context_processors import request
from django.forms.widgets import Widget, CheckboxSelectMultiple
from django.utils.regex_helper import Choice
from cProfile import label

'''
type_CHOICES = (
                ('realtime', '实时流量'),
                ('total', '总流量'),
                ('all', '实时和总流量'),
                ('unlock', '解锁ip'),
                )

class AdminFlow(ModelForm):
    type = forms.ChoiceField(choices=type_CHOICES)
    class Meta:
        model = cmds
        fields = ('ip','name','gp','pid','remask','type','endtime')
        widgets = {
            'endtime': DateTimeWidget(attrs={}, usel10n = True),
             #'endtime': DateTimeWidget(options = dateTimeOptions)
             #'remask':Textarea(attrs={'width':'400px','heigth':'150px'}),
             #'remask': forms.Textarea(attrs={'cols': 80, 'rows': 20}),

            }

    def clean_pid(self):
        pid = self.cleaned_data['pid'].strip().encode('utf-8')

        if pid[0] == 'p' or  pid[0] == 'P':
            pass
        else:
            raise forms.ValidationError('%s  请输入员工编号' % pid)

        if len(pid) != 8:
            raise forms.ValidationError('员工编号位数错误')
        return pid
'''
'''
checkbox_cluster = (
                ('Bjbprdapp01', 'Bjbprdapp01'),
                ('Bjbprdapp02', 'Bjbprdapp02'),
                ('Bjbprdapp03', 'Bjbprdapp03'),
                ('Bjbprdapp04', 'Bjbprdapp04'),

)

Choice_cmds = (
                ('GettenantLbsettings', 'GettenantLbsettings'),
                ('GetNodeEvents', 'GetNodeEvents'),
                ('GetTenantevents', 'GetTenantevents'),
                ('GetTenantContainers', 'GetTenantContainers'),

)

class Fcclient(forms.Form):
    cluster= forms.MultipleChoiceField(required=True, 
                                       widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control','inline': True,'style':'font-size: 18px;',}),
                                       choices=checkbox_cluster,
                                       label="Cluster: ")
    cmd = forms.ChoiceField(required=True,choices=Choice_cmds,label='Command: ',widget=forms.Select(attrs={'class': 'form-control','style':'font-size: 18px;width: 340px;',}))  
    parameter = forms.CharField(required=True,label='Command Parameters: ',widget=forms.Textarea(attrs={'class':"form-control",'aria-describedby':"sizing-addon1",'style':'width: 680px; height: 128px;font-size: 18px;',}))
    
    def clean_ip(self):
        ip = self.cleaned_data['ip'].strip()
        ips = ip.split('.')
        if ips[0] != '192' or ips[1] !='168' or int(ips[2]) > 79 or int(ips[2]) < 65:
            raise forms.ValidationError('Are you CDC Person ?')

        return ip       
  
  '''

#name = forms.CharField(widget=forms.TextInput(attrs={'class': 'special'}))