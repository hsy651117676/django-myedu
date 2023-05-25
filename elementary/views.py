from django.views import View
# from django.shortcuts import render, HttpResponse, redirect
from django.shortcuts import render
# from django.http import HttpResponse, FileResponse
from django.http import JsonResponse
from elementary.models import (
    stu_register_table,
    operation_stu_log,
    stu_school_grade,
    basiceduchoices
)
from base.models import region
from base.mytools import IDCardChecker, is_number
import time
import os
import re
# import json
from django.http import QueryDict
from django.conf import settings
from django.core.paginator import Paginator
from PIL import Image


# Create your views here.
def checkUser(request):
    stu_card = request.GET['card']
    result = stu_register_table.objects.filter(card=stu_card)
    if result.exists():
        return JsonResponse({'msg': 'yes'})
    else:
        return JsonResponse({'msg': 'no'})


def publicitys(request):

    return render(request, 'elementary/publicity.html')


def keyboardsPiano(request):

    return render(request, 'elementary/keyboard_piano.html')


def stuIndex(request):
    return render(request, 'elementary/stu_index.html')


def stuQueryRegister(request):
    stu_card = request.GET.get("card", '')
    name = request.GET.get("name", '')
    if (stu_card + name) == "":
        return render(request, 'elementary/stu_query_index.html')
    else:
        ctx = {}
        ctx['data'] = stu_register_table.objects.filter(card=stu_card)
        ctx['log'] = operation_stu_log.objects.filter(card=stu_card)
        return render(request, 'elementary/stu_query_register.html', ctx)


class stuRegister(View):
    def get(self, request):
        grade = request.GET.get("grade", '0')
        stu_card = request.GET.get("card", '')
        ctx = {}
        ctx['dic'] = {"houseoptions": basiceduchoices.houseoptions,
                      "stuobj": basiceduchoices.stuobj,
                      "relations": basiceduchoices.relations, }
        queryCard = stu_register_table.objects.filter(card=stu_card)
        if queryCard:
            if queryCard.filter(operatortype__in=[0, 4]).exists():
                ctx['data'] = queryCard
                schoolGrade_id = queryCard.values_list('schoolGrade_id')[0][0]
                grade = stu_school_grade.objects.get(
                    id=schoolGrade_id
                ).grade.id
            else:
                return render(request, 'elementary/stu_query.html', {
                    'card': stu_card
                })
        if is_number(grade):
            ctx['sch'] = stu_school_grade.objects.filter(grade=int(grade))
        return render(request, 'elementary/stu_register.html', ctx)

    def post(self, request):
        data = request.POST.dict()
        result = {'msg': ''}
        data.pop('csrfmiddlewaretoken')
        log = {'card': data['card'], 'names': data['name'],
               'times': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
               'edittype': '0', 'resultnotes': '', 'result': ''}
        log['names'] += '(或监护人)'
        try:
            data['schoolGrade'] = stu_school_grade.objects.get(
                id=data['schoolGrade'])
            data['resaddress'] = region.objects.get(mid=data['resaddress'])
            data['regaddress'] = region.objects.get(mid=data['regaddress'])
            dataUpdate = stu_register_table.objects.filter(card=data['card'])
            if dataUpdate.exists():
                log['result'] = '修改信息'
                stu_register_table.objects.filter(
                    card=data['card']).update(**data)
                result = {'msg': '更新成功！'}
            else:
                log['result'] = '首次登记'
                savetable = stu_register_table(**data)
                savetable.save()
                result = {'msg': '添加成功！'}
        except Exception:
            log['result'] += '失败'
            result = {'msg': '数据保存失败，请核实数据！'}
        logtable = operation_stu_log(**log)
        logtable.save()
        return JsonResponse(result, safe=True, json_dumps_params=None)


class ReviewIndex(View):
    def get(self, request):
        ctx = {}
        ctx['dic'] = {"stuobj": basiceduchoices.stuobj,
                      "operator": basiceduchoices.operator, }
        return render(request, 'elementary/review_index.html', ctx)

    def post(self, request):
        name = request.POST.get('stuname', '')
        stu_card = request.POST.get('card', '')
        operatortype = request.POST.get('operatortype', '')
        stuobj = request.POST.get('stuobj', '')
        pageSize = request.POST.get('pageSize', '20')
        pageNumber = request.POST.get('pageNumber', '1')
        field_display = ('card', 'name', 'age', 'stuobj',
                         'operatortype', 'houseoption')
        if stu_card != "":
            table_data = stu_register_table.objects.filter(
                card=stu_card
            ).values(*field_display)
        else:
            user_school = request.user.nick_name
            dic = {"name__contains": name,
                   "operatortype": operatortype,
                   "stuobj": stuobj,
                   "schoolGrade_id": user_school}
            if not re.match(r'[0-9]', user_school):
                dic['schoolGrade_id'] = 0
            if request.user.is_superuser:
                dic.pop('schoolGrade_id')
            if operatortype == "all":
                dic.pop('operatortype')
            if stuobj == "all":
                dic.pop('stuobj')
            table_data = stu_register_table.objects.filter(
                **dic).values(*field_display)
        paginator = Paginator(table_data, pageSize)
        pageCount = paginator.count
        data = list(paginator.page(pageNumber).object_list)
        page = {"pageSize": pageSize,
                "pageNumber": pageNumber,
                "pageCount": pageCount}
        title = ['身份证号', '姓名', '年龄', '登记属性', '审核状态', '住房类型']
        dict = {"data": data, "table_title": title, "page": page}
        return JsonResponse(dict)


class ReviewStuInfo(View):
    def get(self, request):
        stu_card = request.GET.get('card', 0)
        if stu_card:
            ctx = {}
            ctx['data'] = stu_register_table.objects.filter(card=stu_card)
            ctx['log'] = operation_stu_log.objects.filter(card=stu_card)
            ctx['imagename'] = ['1', '2', '3']
        return render(request, 'elementary/review_stu_info.html', ctx)

    def post(self, request):
        stu_card = request.POST.get('card', '')
        operatortype = request.POST.get('operatortype', '')
        operator = request.POST.get('operator', '')
        ctx = {}
        data = stu_register_table.objects.filter(
            card=stu_card,
            operatortype__in=[1]
        ).first()
        if data:
            if data.schoolGrade.id == request.user.nick_name\
                    or request.user.is_superuser:
                data.operatortype = operator
                data.save()
                log = {'card': stu_card, 'names': request.user.first_name,
                       'times': time.strftime("%Y-%m-%d %H:%M:%S",
                                              time.localtime()),
                       'edittype': operator,
                       'resultnotes': operatortype,
                       'result': 'school review'}
                table_log = operation_stu_log(**log)
                table_log.save()
                ctx['msg'] = 'yes'
            else:
                ctx['msg'] = 'no active'
        else:
            ctx['msg'] = 'no exmaine!'
        return JsonResponse(ctx)


def ReviewSeeImage(request):
    stu_card = request.GET.get('card', 0)
    ctx = {}
    ctx["image"] = "/static/stuimage/" + str(stu_card) + "/"
    return render(request, 'elementary/review_see_image.html', ctx)


class ReviewGather(View):
    def get(self, request):
        ctx = {}
        ctx['dic'] = {"stuobj": basiceduchoices.stuobj,
                      "operator": basiceduchoices.operator, }
        return render(request, 'elementary/review_gather.html', ctx)

    def post(self, request):
        name = request.POST.get('stuname', '')
        stu_card = request.POST.get('card', '')
        operatortype = request.POST.get('operatortype', '')
        stuobj = request.POST.get('stuobj', '')
        pageSize = request.POST.get('pageSize', '20')
        pageNumber = request.POST.get('pageNumber', '1')
        field_display = ('card', 'name', 'age', 'stuobj',
                         'operatortype', 'houseoption')
        if stu_card != "":
            table_data = stu_register_table.objects.filter(
                card=stu_card
            ).values(*field_display)
        else:
            user_school = request.user.nick_name
            dic = {"name__contains": name,
                   "operatortype": operatortype,
                   "stuobj": stuobj,
                   "schoolGrade_id": user_school}
            if not re.match(r'[0-9]', user_school):
                dic['schoolGrade_id'] = 0
            if request.user.is_superuser:
                dic.pop('schoolGrade_id')
            if operatortype == "all":
                dic.pop('operatortype')
            if stuobj == "all":
                dic.pop('stuobj')
            table_data = stu_register_table.objects.filter(
                **dic).values(*field_display)
        paginator = Paginator(table_data, pageSize)
        pageCount = paginator.count
        data = list(paginator.page(pageNumber).object_list)
        page = {"pageSize": pageSize,
                "pageNumber": pageNumber,
                "pageCount": pageCount}
        title = ['身份证号', '姓名', '年龄', '登记属性', '审核状态', '住房类型']
        dict = {"data": data, "table_title": title, "page": page}
        return JsonResponse(dict)


class stuUploadImage(View):
    def get(self, request):
        stu_card = request.GET.get('card', '')
        data = stu_register_table.objects.filter(
            card=stu_card, operatortype__in=[0, 4])
        if data:
            ctx = {}
            ctx['data'] = data
            return render(request, 'elementary/stu_upload_image.html', ctx)
        else:
            return render(request, 'elementary/stu_index.html')

    def post(self, request):
        if compressJPG(request):
            return JsonResponse({'msg': '文件上传成功！'})
        else:
            return JsonResponse({'msg': '文件上传失败, 请检查文件类型!'})

    def put(self, request):
        ctx = QueryDict(request.body).dict()
        data = stu_register_table.objects.filter(
            card=ctx['card'],
            operatortype__in=[0, 4]
        )
        if data:
            data.update(operatortype=1)
            return JsonResponse({'msg': '数据保存成功，请等待学校审核！'})
        else:
            return JsonResponse({'msg': '数据保存失败！'})


def compressJPG(request):
    stu_card = request.POST.get('card', '')
    if not IDCardChecker(stu_card).is_valid():
        return False
    path = os.path.join(settings.STUIMAGE + '/' + stu_card)
    if not os.path.exists(path):
        os.makedirs(path)
    paid = request.POST.get('paid', '')
    num = 1
    for img in request.FILES.getlist('files'):
        img_path = os.path.join(path, paid + "_" + str(num) + '.jpg')
        with open(img_path, 'wb') as fp:
            for chunk in img.chunks():
                fp.write(chunk)
        im = Image.open(img_path)
        (x, y) = im.size
        x_1 = 165
        y_1 = int(y * x_1 / x)
        out = im.resize((x_1, y_1), Image.ANTIALIAS)
        if out.mode == 'RGBA':
            out = out.convert('RGB')
        out.save(path + '/' + paid + "_" + str(num) + 'x.jpg')
        num += 1
    return True


def downloadToExcel(request):
    return render(request, 'elementary/.html')
