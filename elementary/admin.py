from django.contrib import admin
from elementary.models import (stu_register_table,
                               operation_stu_log,
                               stu_grades,
                               stu_schools,
                               stu_school_grade)
# Register your models here.


@admin.register(stu_register_table)
class stuRegisterTableAdmin(admin.ModelAdmin):
    list_display = ['name', 'card', 'age',
                    'schoolGrade', 'stuobj', 'operatortype']
    list_display_links = ('name', )


@admin.register(operation_stu_log)
class operationStuLogAdmin(admin.ModelAdmin):
    list_display = ['names', 'card', 'edittype', 'times',
                    'result', 'resultnotes']
    list_display_links = ('names', )


@admin.register(stu_grades)
class stu_gradesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ('name', )


@admin.register(stu_schools)
class stu_schoolsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ('name', )


@admin.register(stu_school_grade)
class stu_school_grade(admin.ModelAdmin):
    list_display = ['id', 'school', 'grade']
    list_display_links = ('school', )
