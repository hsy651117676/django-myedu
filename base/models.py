# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class userBase(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u"单位名称",
                                 default="")
    birday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    address = models.CharField(max_length=100, verbose_name="单位地址",
                               default=u"")
    mobile = models.CharField(max_length=11, verbose_name="联系电话",
                              null=True, blank=True)
    image = models.ImageField(upload_to="image/%Y/%m",
                              default=u"image/default.png",
                              max_length=100,
                              verbose_name="头像")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class menu(models.Model):
    melement = models.CharField(max_length=150, verbose_name="element",
                                default="")
    mhref = models.CharField(max_length=150, verbose_name="href",
                             null=True, blank=True)
    msrc = models.CharField(max_length=150, verbose_name="src",
                            null=True, blank=True)
    mclass = models.CharField(max_length=150, verbose_name="class",
                              null=True, blank=True)
    mdataoption = models.CharField(max_length=150, verbose_name="dataOption",
                                   null=True, blank=True)
    mtitle = models.CharField(max_length=150, verbose_name="title", default="")
    mstyle = models.CharField(max_length=150, verbose_name="style", null=True,
                              blank=True)
    level = models.CharField(max_length=150, verbose_name="level", default="")
    pid = models.CharField(max_length=150, verbose_name="pid", default="")
    mid = models.CharField(max_length=150, verbose_name="mid", default="")

    class Meta:
        verbose_name = "菜单管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.mtitle


class region(models.Model):
    mid = models.CharField(max_length=12, verbose_name="mid", primary_key=True)
    pid = models.CharField(max_length=12, verbose_name="pid", default="")
    addressShort = models.CharField(max_length=50, verbose_name="地址简称",
                                    default="")
    addressAll = models.CharField(max_length=150, verbose_name="地址全称",
                                  default="")
    level = models.IntegerField(verbose_name="级别")

    class Meta:
        verbose_name = "行政区划表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.addressShort
