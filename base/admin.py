from django.contrib import admin
from base.models import *
# Register your models here.
admin.site.site_header='后台管理系统' 
admin.site.site_title='后台管理系统' 
admin.site.index_title='首页'


@admin.register(menu)
class menuAdmin(admin.ModelAdmin):
    list_display=['mtitle','melement','mhref','msrc','mclass','mdataoption','mstyle','level','pid','mid']
    list_display_links=('mtitle',)

@admin.register(userBase)
class userBaseAdmin(admin.ModelAdmin):
    list_display=['username','first_name','nick_name','mobile','is_active']
    list_display_links=('username',)

@admin.register(region)
class userBaseAdmin(admin.ModelAdmin):
    list_display=['pid','mid','addressShort','addressAll','level']
    list_display_links=('mid',)

