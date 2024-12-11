from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

## Create your views here.

def index(request):
    return render (request, 'main/base.html', {})

def homepage(request):
    return render(request, 'main/home.html', {})
    # primjetiti korištenje HTML-a


