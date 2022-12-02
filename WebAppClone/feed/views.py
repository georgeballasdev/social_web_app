from django.shortcuts import HttpResponse, render

def homeview(request):
    return HttpResponse('Home feed page')
