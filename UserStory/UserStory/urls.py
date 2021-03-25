"""UserStory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import api
from UserModel.views import log_up, log_in, log_out
urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', api.Hello),
    path('log_up/', log_up),
    path('log_in/', log_in),
    path('log_out/', log_out),
    path('chat/', include('Trim.urls'))
]
