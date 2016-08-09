from django.shortcuts import render,render_to_response

# Create your views here.
from django.http import HttpResponse
import c
'''
def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    return render_to_response('index.html',{})
'''
import time

from django.template import RequestContext
def home_user(request):
    #return HttpResponse("Wating done.")
    #return render_to_response('home.html',{'user.username':request}, context_instance = RequestContext(request))
    #return render_to_response('home.html',{'user.username':request}, context_instance = RequestContext(request))
    return render(request, 'home.html')
from django.core.urlresolvers import reverse
from django.http import JsonResponse

def conta(request):
    c.prova(0)
    redirect = reverse('home')
    return JsonResponse({'redirect':redirect})


def ajax_list(request):
    a = range(100)
    return JsonResponse(a, safe=False)
 
def ajax_dict(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return JsonResponse(name_dict)

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index22.html')
    
def add(request):
    a = request.GET['a']
    b = request.GET['b']
    a = int(a)
    b = int(b)
    return HttpResponse(str(a+b))
def t(request):
    return render(request, 't.html')
    
    
