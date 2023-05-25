from django.shortcuts import render

# Create your views here.


def stuIndex(request):
    return render(request, 'supports/stu_index.html')
