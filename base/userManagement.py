import os
import json,requests,time
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
from django.views.decorators import csrf
from django.contrib.auth import  login
from django.contrib.auth.models import User,Group 
from base.models import * 
from base import mytools

def add_user(request):
    mydata =userBase.objects.values()
    # mydata =userBase.objects.filter(id=1).values()
    return render(request, "base/adduser.html", {"mydata":mydata})
