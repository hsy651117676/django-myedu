from django.db import models
from base.models import region
# from mdeditor.fields import MDTextField


class basiceduchoices():
    stuobj = (
        (1, '户籍所在地属于划片范围内的适龄人员'),
        (2, '外省外县进城务工随迁子女（家长务工就业或经商）'),
        (3, '盘州市内进城务工子女（家长务工就业或经商）'),
        (4, '烈士子女、驻盘部队的现役军人子女、公安英模和因公牺牲、伤残警察子女'),
        (5, '参加抗疫最前线的医护人员的子女'),
        (6, '易地扶贫搬迁子女'),
    )
    operator = (
        (0, '未上传资料或未提交'),
        (1, '提交待初审'),
        (2, '初审通过'),
        (3, '审核不通过（不允许再次提交）'),
        (4, '审核不通过（驳回修改)'),
        (5, '复审通过'),
        (6, '复审不通过'),
    )
    houseoptions = (
        (0, '购房'),
        (1, '租房'),
        (2, '自建房'),
    )
    relations = (
        (1, '无'),
        (2, '父亲'),
        (3, '母亲'),
        (4, '爷爷'),
        (5, '奶奶'),
        (6, '外公'),
        (7, '外婆'),
        (12, '亲哥'),
        (13, '亲嫂'),
        (14, '表哥'),
        (15, '表嫂'),
        (16, '堂哥'),
        (17, '堂嫂'),
        (18, '亲姐'),
        (19, '亲姐夫'),
        (20, '表姐'),
        (21, '表姐夫'),
        (22, '堂姐'),
        (23, '堂姐夫'),
        (24, '伯父'),
        (25, '伯母'),
        (26, '叔父'),
        (27, '婶母'),
        (28, '舅父'),
        (29, '舅母'),
        (30, '姨父'),
        (31, '姨母'),
        (32, '姑父'),
        (33, '姑母'),
        (34, '其他亲属'),
        (35, '非亲属'),
    )


class stu_grades(models.Model):
    id = models.PositiveSmallIntegerField(verbose_name='年级', primary_key=True)
    name = models.CharField(max_length=50, verbose_name='年级名称')

    class Meta:
        verbose_name = '年级名称表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class stu_schools(models.Model):
    id = models.PositiveSmallIntegerField(verbose_name='学校编号', primary_key=True)
    name = models.CharField(max_length=50, verbose_name='学校名称')

    class Meta:
        verbose_name = '学校名称表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class stu_school_grade(models.Model):
    id = models.PositiveSmallIntegerField(verbose_name='序号', primary_key=True)
    school = models.ForeignKey(stu_schools, null=True, db_constraint=False,
                               related_name='schoolname', on_delete=models.SET_NULL)
    grade = models.ForeignKey(stu_grades, null=True, db_constraint=False, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = '学校年级名称总表'
        verbose_name_plural = verbose_name
        unique_together = ['school', 'grade']

    def __str__(self):
        return self.school.name + self.grade.name


class stu_register_table(models.Model):
    id = models.AutoField(
        primary_key=True)
    name = models.CharField(
        max_length=20, null=True, unique=False, verbose_name='学生姓名')
    card = models.CharField(
        max_length=18, null=True, unique=False, verbose_name='学生身份证号')
    age = models.IntegerField(
        null=True, verbose_name='年龄')
    schoolGrade = models.ForeignKey(
        stu_school_grade, null=True, db_constraint=False,
        on_delete=models.SET_NULL)
    jfr1name = models.CharField(
        max_length=20, null=True, unique=False, verbose_name='监护人1姓名')
    jfr1gx = models.PositiveSmallIntegerField(
        verbose_name='监护人1与登记人关系', choices=basiceduchoices.relations)
    jfr1tel = models.CharField(
        max_length=11, null=True, unique=False, verbose_name='监护人2联系电话')
    jfr2name = models.CharField(
        max_length=20, null=True, unique=False, verbose_name='监护人2姓名')
    jfr2gx = models.PositiveSmallIntegerField(
        verbose_name='监护人2与登记人关系',
        choices=basiceduchoices.relations, null=True)
    jfr2tel = models.CharField(
        max_length=11, null=True, unique=False, verbose_name='监护人2联系电话')
    regaddress = models.ForeignKey(
        region, null=True, db_constraint=False,
        on_delete=models.SET_NULL,
        related_name='reg', verbose_name='户籍所在地')
    resaddress = models.ForeignKey(
        region, null=True, db_constraint=False,
        on_delete=models.SET_NULL,
        related_name='res', verbose_name='居住所在地')
    resaddressnum = models.CharField(
        max_length=100, null=True, unique=False, verbose_name='居住地详细地址')
    stuobj = models.PositiveSmallIntegerField(
        verbose_name='登记对象属性', choices=basiceduchoices.stuobj)
    houseoption = models.PositiveSmallIntegerField(
        verbose_name='预登记学生现住房类型', choices=basiceduchoices.houseoptions)
    operatortype = models.IntegerField(
        '操作状态', default=0, choices=basiceduchoices.operator)
    publicid = models.IntegerField(
        '是否公示', default=0)

    class Meta:
        verbose_name = '预登记情况总表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class operation_stu_log(models.Model):
    card = models.CharField(
        max_length=18, null=True, unique=False, verbose_name='学生身份证号')
    edittype = models.IntegerField(
        '操作状态', default=0, choices=basiceduchoices.operator)
    names = models.CharField(
        max_length=11, null=True, unique=False, verbose_name='操作人')
    times = models.CharField(
        max_length=20, null=True, unique=False, verbose_name='操作时间')
    result = models.CharField(
        max_length=100, null=True, unique=False, verbose_name='操作结果')
    resultnotes = models.CharField(
        max_length=200, null=True, unique=False, verbose_name='操作情况补充说明')

    class Meta:
        verbose_name = '预登记情况操作日志'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.names


class infant_stu(models.Model):
    id = models.AutoField(
        primary_key=True)
    name = models.CharField(
        max_length=20, null=True, unique=False, verbose_name='学生姓名')
    card = models.CharField(
        max_length=18, null=True, unique=False, verbose_name='学生身份证号')
    age = models.IntegerField(
        '年龄')
    regaddress = models.CharField(
        max_length=100, null=True, unique=False, verbose_name='户籍所在地')
    resaddress = models.CharField(
        max_length=100, null=True, unique=False, verbose_name='居住所在地')
    regsch = models.CharField(
        max_length=100, null=True, unique=False, verbose_name='意向学校')
    tel = models.CharField(
        max_length=11, null=True, unique=False, verbose_name='联系电话')

    class Meta:
        verbose_name = '幼儿园入学意向调查表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
