# -*- coding: utf-8 -*-

from collections import OrderedDict
from kook.models import RootFactory

def nav(request):
    return OrderedDict([
        (u'главная', '/'),
        (u'добавить рецепт', request.route_path('create_recipe'))
    ])

def handle_new_request(event):
    event.request.nav = nav(event.request)
    event.request.root = RootFactory(event.request)