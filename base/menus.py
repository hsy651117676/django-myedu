# import requests
from django.shortcuts import render
from base.models import menu
# from base import mytools


def main_menu(user):
    menus = ""
    if user.groups.filter(name='系统管理员组').exists():
        menus = menus + menutree('01')
    if user.groups.filter(name='人事管理组').exists():
        menus = menus + menutree('02')
    if user.groups.filter(name='特教组').exists():
        menus = menus + menutree('11')
    if user.groups.filter(name='资助管理组').exists():
        menus = menus + menutree('12')
    if user.groups.filter(name='基础教育组').exists():
        menus = menus + menutree('13')
    if user.groups.filter(name='教学质量组').exists():
        menus = menus + menutree('14')
    menus = menus + menutree('10')  # Menus displayed by all users
    return menus


def menutree(mpid):
    div1 = menu.objects.filter(level=1, pid=mpid)
    menuhtml = ''
    for var in div1:
        level2 = ''
        btn = menu.objects.filter(level=2, pid=var.mid)
        for a in btn:
            abtn = '<' + a.melement + ' href="' + a.mhref + '" src="' + a.msrc + '" class="' + \
                a.mclass + '" data-options="' + a.mdataoption + '" >' + a.mtitle + '</' + \
                a.melement + '>'
            level2 = level2 + abtn
        level1 = '<' + var.melement + ' title="' + var.mtitle + '" data-options="' + \
            var.mdataoption + '" style="' + var.mstyle + '">' + level2 + '</' + var.melement + '>'
        menuhtml = menuhtml + level1
    return menuhtml


# When the menu item in the database is empty,
# initialize the menu in the database and add some examples
def menu_edit(request):
    menucount = menu.objects.values().count()
    if menucount == 0:
        menu(melement='div', mtitle='系统管理', mdataoption="iconCls:'icon-large-shapes'",
             mstyle='padding:0px;', level='1', pid='01', mid='0101').save()
        menu(melement='a', mtitle='菜单管理', mdataoption="iconCls:'icon-large-shapes'",
             mstyle='padding:0px;', level='2', pid='0101', mid='0101001',
             mhref="javascript:void(0)", msrc='/base/menuedit',
             mclass="easyui-linkbutton cs-navi-tab").save()
        menu(melement='div', mtitle='帮助', mdataoption="iconCls:'icon-help'",
             mstyle='padding:0px;', level='1', pid='10', mid='1001').save()
        menu(melement='a', mtitle='电脑键盘钢琴', mdataoption="iconCls:'icon-large-shapes'",
             mstyle='padding:0px;', level='2', pid='1001', mid='1001001',
             mhref="javascript:void(0)", msrc='/base/keyboards',
             mclass="easyui-linkbutton cs-navi-tab").save()
        menu(melement='a', mtitle='关于我……', mdataoption="iconCls:'icon-large-shapes'",
             mstyle='padding:0px;', level='2', pid='1001', mid='1001002',
             mhref="javascript:void(0)", msrc='/base/about',
             mclass="easyui-linkbutton cs-navi-tab").save()
        menu(melement='a', mtitle='常用网站', mdataoption="iconCls:'icon-search'",
             mstyle='padding:0px;', level='2', pid='1001', mid='1001003',
             mhref="javascript:void(0)", msrc='/base/about',
             mclass="easyui-linkbutton cs-navi-tab").save()
    mydata = menu.objects.values()
    return render(request, "base/menuedit.html", {"mydata": mydata})
