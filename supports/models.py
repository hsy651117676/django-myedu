from django.db import models
from base.models import region

# Create your models here.


class stu_register(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=20, null=True, unique=False, verbose_name='学生姓名')
    card = models.CharField(
        max_length=18, null=True, unique=False, verbose_name='学生身份证号')
    age = models.IntegerField(
        null=True, verbose_name='年龄')
    # schoolGrade = models.ForeignKey(
    #     stu_school_grade, null=True, db_constraint=False,
    #     on_delete=models.SET_NULL)
    # jfr1name = models.CharField(
    #     max_length=20, null=True, unique=False, verbose_name='监护人1姓名')
    # jfr1gx = models.PositiveSmallIntegerField(
    #     verbose_name='监护人1与登记人关系', choices=basiceduchoices.relations)
    # jfr1tel = models.CharField(
    #     max_length=11, null=True, unique=False, verbose_name='监护人2联系电话')
    # jfr2name = models.CharField(
    #     max_length=20, null=True, unique=False, verbose_name='监护人2姓名')
    # jfr2gx = models.PositiveSmallIntegerField(
    #     verbose_name='监护人2与登记人关系',
    #     choices=basiceduchoices.relations, null=True)
    # jfr2tel = models.CharField(
    #     max_length=11, null=True, unique=False, verbose_name='监护人2联系电话')
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

    class Meta:
        verbose_name = '预登记情况总表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

