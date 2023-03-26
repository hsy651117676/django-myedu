import os
import json
import requests
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from django.views.decorators import csrf
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from base.models import *
from base import mytools


def main_menu(user):
    menus = ""
    if user.groups.filter(name='系统管理员组').exists():
        menus = menus + menutree('01')
    if user.groups.filter(name='特教组').exists():
        menus = menus + menutree('11')
    if user.groups.filter(name='教学质量组').exists():
        menus = menus + menutree('12')
    if user.groups.filter(name='人事管理组').exists():
        menus = menus + menutree('02')
    if user.groups.filter(name='基础教育组').exists():
        menus = menus + menutree('13')
    menus = menus + menutree('10')  # All users display a menu
    return menus


def menutree(mpid):
    div1 = menu.objects.filter(level=1, pid=mpid)
    menuhtml = ''
    for var in div1:
        level2 = ''
        btn = menu.objects.filter(level=2, pid=var.mid)
        for a in btn:
            abtn = '<' + a.melement + ' href="' + a.mhref + '" src="' + a.msrc + '" class="' + \
                a.mclass + '" data-options="' + a.mdataoption + '" >' + a.mtitle + '</' + a.melement + '>'
            level2 = level2 + abtn
        level1 = '<' + var.melement + ' title="' + var.mtitle + '" data-options="' + \
            var.mdataoption + '" style="' + var.mstyle + '">' + level2 + '</' + var.melement + '>'
        menuhtml = menuhtml + level1
    return menuhtml


def menu_edit(request):
    menucount = menu.objects.values().count()
    if menucount == 0:
        menu(melement='div', mtitle='系统管理', mdataoption="iconCls:'icon-large-shapes'",
             mstyle='padding:0px;', level='1', pid='01', mid='01').save()
        menu(melement='a', mtitle='菜单管理', mdataoption="iconCls:'icon-large-shapes'", mstyle='padding:0px;', level='2', pid='01', mid='0101',
             mhref="javascript:void(0)", msrc='/base/menuedit', mclass="easyui-linkbutton cs-navi-tab").save()
    mydata = menu.objects.values()
    return render(request, "base/menuedit.html", {"mydata": mydata})
