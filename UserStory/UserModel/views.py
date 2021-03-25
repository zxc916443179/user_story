from django.shortcuts import render
from hashlib import md5
# Create your views here.
from UserStory.api import APIFunction, APIError
from .controller import UserController
@APIFunction
def log_up(username, password):
    user = UserController.create(username, password)
    return user

@APIFunction
def log_in(username, password, session):
    users = UserController.get_by_username(username)
    if len(users) == 0:
        raise APIError(201)
    if md5(password.encode('utf-8')).hexdigest() != users[0].password:
        raise APIError(202)
    user = users[0]
    session['user_session'] = user.username
    return users[0]
@APIFunction
def log_out(session):
    session['user_session'] = None
    return ''

