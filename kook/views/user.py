# -*- coding: utf-8 -*-

import json
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from kook.models.user import User, Profile
from kook import caching


def check_matchdict(param, request):
    if param in request.matchdict:
        return request.matchdict[param]
    return False


def register_view(request):
    response = dict()
    next_url = check_matchdict('next_path', request) or \
        request.route_path('dashboard')
    response['register_path'] = '/register'
#    if request.POST:
#        result = User.construct_from_dict(request.POST.mixed())
#        if isinstance(result, User):
#            result.groups = [Group('registered')]
#            result.save()
#            request.session.flash(u'<div class="alert alert-success">'
#                                  u'Вы зарегистрированы и авторизованы!'
#                                  u'</div>')
#            headers = remember(request, result.id)
#            return HTTPFound(next, headers=headers)
#        else:
#            request.session.flash(u'<div class="alert alert-error">'
#                                  u'Ошибка при регистрации'
#                                  u' пользователя!</div>')
#            response['error_data'] = json.dumps(result)
    return response


def login_view(request):
    next_url = check_matchdict('next_path', request) or\
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
            return HTTPFound(location=next_url, headers=headers)
        else:
            request.session.flash(u'<div class="alert alert-error">'
                                  u'Авторизация не удалась!'
                                  u'</div>')
    return dict()


def logout_view(request):
    next_url = request.route_url('login')
    headers = forget(request)
    return HTTPFound(next_url, headers=headers)


def update_profile_view(request):
    response = dict()
    response['profile'] = request.user.profile
    if request.POST:
        result = Profile.construct_from_multidict(
            request.POST, current_profile=response['profile'])
        user = request.user
        try:
            user.profile = result
            user.save()
            caching.clear_user(user.id)
            response['profile'] = user.profile
            request.session.flash(u'<div class="alert alert-success">'
                                  u'Профиль обновлен!</div>')
        except AttributeError:
            request.session.flash(u'<div class="alert alert-error">'
                                  u'Ошибка при обновлении профиля!</div>')
            response['error_data'] = json.dumps(result)
    return response
