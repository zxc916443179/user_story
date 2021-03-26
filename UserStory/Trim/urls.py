# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('trim/', views.trim, name='trim'),
    path('trim/file_download/', views.file_download),
    path('', views.index, name='index')
]