"""main URL Configuration

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
from base import views
from base.views import page_error, page_not_found, permission_denied
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# from django.views.generic.base import RedirectView
# from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view),

    path('captcha', include('captcha.urls')),

    path('base/', include('base.urls')),

    path('elementary/', include('elementary.urls')),

    path('supports/', include('supports.urls')),

    path('login/', views.login_view),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index_view, name='index'),

]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler403 = permission_denied
handler404 = page_not_found
handler500 = page_error
