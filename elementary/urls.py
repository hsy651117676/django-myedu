"""elementary URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from elementary.views import *
from django.urls import path

urlpatterns = [
    path('Review/Index', ReviewIndex.as_view(), name='review_index'),
    path('Review/StuInfo', ReviewStuInfo.as_view(), name='review_stuInfo'),
    path('Review/SeeImage', ReviewSeeImage, name='review_see_image'),
    path('Review/Gather', ReviewGather.as_view(), name='reaview_gather'),

    path('stu/index', stuIndex, name='stu_index'),
    path('stu/checkuser', checkUser, name='stu_check_user'),
    path('stu/Register', stuRegister.as_view(), name='stu_register'),
    path('stu/QueryRegister', stuQueryRegister, name='stu_query_register'),
    path('stu/publicity', publicitys, name='stu_publicity'),
    path('stu/UploadImage', stuUploadImage.as_view(), name='stu_upload_image'),

    path('stu/keyboardpiano', keyboardsPiano, name='keyboardPiano'),

]
