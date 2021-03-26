from django.shortcuts import render
from django.shortcuts import render
from hashlib import md5
from os import path
from django.http import FileResponse, HttpResponseBase
# Create your views here.
from UserStory.api import APIFunction, APIError
@APIFunction
def trim(request):
    return render(request, 'trim/test.html')
@APIFunction
def index(request):
    return render(request, 'trim/index.html')
@APIFunction
def file_download(session):
    username = session['user_session']
    filename = f"out_t_{username}.mp4"
    file_path = '.'
    vid = open(path.join(file_path, filename), 'rb')
    response = FileResponse(vid)	
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']=f'attachment;filename={filename}'
    return response
