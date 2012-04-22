# -*- coding: utf-8 -*-

import json
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget, authenticated_userid
from ..models import User

def check_matchdict(param, request):
    if param in request.matchdict:
        return request.matchdict[param]
    return False

def register_view(request):
    response = dict()
    next = check_matchdict('next_path', request) or\
           request.route_path('dashboard')
    response['register_path'] = '/register'
    if request.POST:
        result = User.construct_from_multidict(request.POST)
        if isinstance(result, User):
            result.save()
            request.session.flash(u'<div class="alert alert-success">'
                                  u'Пользователь "%s" зарегистрирован!'
                                  u'</div>' % result.email)
            headers = remember(request, result.email)
            return HTTPFound(next, headers=headers)
        else:
            request.session.flash(u'<div class="alert alert-error">'
                                  u'Ошибка при регистрации'
                                  u' пользователя!</div>')
            response['error_data'] = json.dumps(result)
    return response

def login_view(request):
    next = check_matchdict('next_path', request) or\
           request.route_path('dashboard')
    if request.POST:
        email = request.POST.getone('email')
        password = request.POST.getone('password')
        user = User.fetch(email=email)
        if user and user.check_password(password):
            headers = remember(request, user.id)
            request.session.flash(u'<div class="alert alert-success">'
                                  u'Добро пожаловать!'
                                  u'</div>')
            return HTTPFound(location=next, headers=headers)
        else:
            request.session.flash(u'<div class="alert alert-error">'
                                  u'Авторизация не удалась!'
                                  u'</div>')
    return dict()

def logout_view(request):
    next = request.route_url('login')
    headers = forget(request)
    return HTTPFound(next, headers=headers)