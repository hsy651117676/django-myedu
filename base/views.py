import os
import json
import time
import ast
from django.http import HttpResponse, FileResponse
from django.views.decorators.cache import cache_page
from django.core.mail import EmailMessage
# from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
# from django.views.decorators import csrf
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django import forms
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import Group
from django.db.models import Q, F
from django.views.decorators.csrf import csrf_exempt

from captcha.fields import CaptchaField, CaptchaStore

from base import menus
from base import mytools
from base.models import userBase, region


class UserForm(forms.Form):
    captcha = CaptchaField(label='验证码', required=True,
                           error_messages={'required': '验证码不能为空'})


def index_view(request):
    status = request.COOKIES.get('is_login')
    if not status:
        return redirect("/login/")
    if not request.user.is_authenticated:
        return redirect("/login/")
    ctx = {}
    menu = menus.main_menu(request.user)
    ctx['dic'] = {"menu": menu}
    return render(request, "index.html", ctx)


def login_view(request):
    register_form = UserForm(request.POST)
    if register_form.is_valid():
        pass
    register_form = UserForm()
    if request.method == "GET":
        return render(request, "login.html", {'register_form': register_form})
    username = request.POST.get("username")
    password = request.POST.get("pswd")
    key = request.POST.get("captcha_0")
    code = request.POST.get("captcha_1")
    captcha_obj = CaptchaStore.objects.filter(hashkey=key).values().count()
    user = authenticate(username=username, password=password)
    if user and captcha_obj != 1:
        auth.login(request, user)
        rep = redirect("/index/")
        rep.set_signed_cookie("is_login", user, salt='is_login_jmy',
                              max_age=60*30)
        rep.user = user
        return rep
    else:
        users = userBase.objects.filter(username=username,
                                        is_active=False).values()
        if users.exists():
            return render(request, "login.html",
                          {'msg': '用户未激活，请登录注册邮箱激活!',
                           'register_form': register_form}
                          )
        else:
            return render(request, "login.html",
                          {'msg': '请核实用户名、密码、验证码',
                           'register_form': register_form}
                          )


def logout_view(request):
    auth.logout(request)
    rep = redirect('/login/')
    rep.delete_cookie("is_login")
    request.session.flush()
    return rep


def active(request, parameter):
    try:
        jm = mytools.AEScoder()
        aes = jm.decrypt(parameter)
    except Exception:
        return redirect("/login/")
    else:
        user_dict = ast.literal_eval(aes)
        username = user_dict['user']
        mytime = float(user_dict['time'])
        nowtime = float(time.time())
        mytime = int((nowtime - mytime) / 3600)
        ctx = {}
        if mytime <= 1:
            user = userBase.objects.get(username=username)
            user.is_active = True
            user.save()
            ctx['msg'] = "用户激活成功！"
        else:
            ctx['msg'] = "链接已失效!"
        return render(request, 'base/msg.html', ctx)


def msg(request):
    return render(request, 'base/msg.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['user']
        first_name = request.POST['name']
        card = request.POST['card']
        phone = request.POST['tel']
        email = request.POST['email']
        message = request.POST['message']
        password = make_password(request.POST['pwd'])
        group = request.POST['group']
        usercreate = userBase.objects.create(
                username=username, first_name=first_name,
                card=card, phone=phone, email=email,
                message=message, password=password)
        usercreate.is_active = 0
        usercreate.save()
        if group == '1':
            pass
        elif group == '5':
            print(group)
            g = Group.objects.get(name='教学质量组')
            g.user_set.add(usercreate)
        else:
            pass
        if usercreate:
            oldstr = {'user': usercreate.username,
                      'time': str(time.time())
                      }
            jm = mytools.AEScoder()
            aes = jm.encrypt(oldstr)
            subject = "用户激活"
            message = '''<h1>{}, 欢迎您</h1>请点击下面链接激活您的账户<br/>
            <a href="https: //218.201.223.229: 8888/active/{}">点我激活</a></br>
            https: //218.201.223.229: 8888/active/{}
            '''.format(first_name, aes, aes)
            sender = settings.EMAIL_FROM
            receiver = [email]
            msg = EmailMessage(subject, message, sender, receiver)
            msg.content_subtype = 'html'
            msg.send()
            return redirect("/login/")
    else:
        return render(request, 'register.html')


def forget(request):
    if request.method == 'POST':
        username = request.POST['user']
        card = request.POST['card']
        phone = request.POST['tel']
        email = request.POST['email']
        password = make_password(request.POST['pwd'])
        user = userBase.objects.filter(
                username=username, card=card, phone=phone, email=email).first()
        if user:
            user.password = password
            user.save()
            return redirect("/login/")
        else:
            return redirect("/login/")
    else:
        return render(request, 'forget.html')


def checkUser(request):
    user = request.POST['user']
    result = userBase.objects.filter(username=user)
    if result.exists():
        return JsonResponse({'msg': 'yes'})
    else:
        return JsonResponse({'msg': 'no'})


def page_not_found(request, exception):
    return render(request, 'base/404.html')


def page_error(request):
    return render(request, 'base/500.html')


def permission_denied(request, exception):
    return render(request, 'base/403.html')


def file_response_download(request):
    file_path = 'media/' + request.GET.get('file_path')
    response = FileResponse(open(file_path, 'rb'))
    response['content_type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment; filename='\
        + os.path.basename(file_path)
    return response


def help_webs(request):
    ctx = {}
    table_title = ['类别', '网站名称', '网址']
    ctx['dic'] = {"url": "help_webs/",
                  "name": "学校名称", "card": "学校标识码", "mytitle": "",
                  "table_title": table_title}
    return render(request, "base/webs.html", ctx)


def help_webs_ajax(request):
    pageNumber = request.POST['pageNumber']
    pageSize = request.POST['pageSize']
    p1 = request.POST['PA1']
    webs = {}
    mydata = webs.objects.filter(Q(category__contains=p1)).values()
    total = mydata.count()
    rows = list(mydata)
    resList = {"total": total, "rows": rows}
    ulist = json.dumps(resList, ensure_ascii=False)
    return HttpResponse(ulist)


def schoolBase(request):
    name = request.GET.get('pa1', '')
    township = request.GET.get('pa2', '0')
    period = request.GET.get('pa3', '0')
    pageNumber = request.GET.get('pageNumber', 1)
    pageSize = request.GET.get('pageSize', 30)
    from analysis.models import schoolBase
    from django.core.paginator import Paginator
    if township == '0':
        if period == '0':
            data = schoolBase.objects.filter(name__contains=name)
        else:
            data = schoolBase.objects.filter(
                    name__contains=name, township=township)
    else:
        if period == '0':
            data = schoolBase.objects.filter(
                    name__contains=name, township=township)
        else:
            data = schoolBase.objects.filter(
                    name__contains=name, township=township, period=period)
    paginator = Paginator(data, pageSize)
    page_data = paginator.get_page(pageNumber)
    data = page_data.object_list
    ctx = {
        'data': data,
        'title': mytools.mychoices.titlebaseschool,
        'total': paginator.count,
        'pageNumber': pageNumber,
        'pageSize': pageSize,
        'township': mytools.mychoices.township,
        'period': mytools.mychoices.period,
        'pas': '?pa1=' + name + "&pa2=" + township + "&pa3=" + period,
        'oldpa': [name, township, period]
        }
    return render(request, "base/base_school.html", ctx)


@csrf_exempt
@cache_page(24*60*60)
def queryRegion(request):
    pid = request.GET.get('pid')
    level = request.GET.get('level')
    mid = request.GET.get('mid', '')
    if level == '1':
        data = region.objects.filter(level=level).values(
                'pid', 'level', 'addressAll',
                text=F('addressShort'), id=F('mid'))
    elif mid != "":
        data = region.objects.filter(mid=mid+"000000").values(
                'pid', 'level', 'addressAll',
                text=F('addressShort'), id=F('mid'))
    else:
        data = region.objects.filter(pid=pid, level=level).values(
                'pid', 'level', 'addressAll',
                text=F('addressShort'), id=F('mid'))
    mydata = json.dumps(list(data))
    return HttpResponse(mydata)


def page_not_found(request, exception):
    return render(request, 'base/404.html')


def page_error(request):
    return render(request, 'base/500.html')


def permission_denied(request, exception):
    return render(request, 'base/403.html')


def file_response_download(request):
    file_path = 'media/' + request.GET.get('file_path')
    response = FileResponse(open(file_path, 'rb'))
    response['content_type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment; filename='\
        + os.path.basename(file_path)
    return response
