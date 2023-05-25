from django.contrib import admin
from supports.models import (stu_register,)


# Register your models here.
@admin.register(stu_register)
class stuRegisterTableAdmin(admin.ModelAdmin):
    list_display = ['name', 'card', 'age',
                    ]
    list_display_links = ('name', )

