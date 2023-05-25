from django.shortcuts import render
from base.models import userBase


def add_user(request):
    mydata = userBase.objects.values()
    # mydata =userBase.objects.filter(id=1).values()
    return render(request, "base/adduser.html", {"mydata": mydata})
