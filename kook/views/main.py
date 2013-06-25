# -*- coding: utf-8 -*-

from kook.models.recipe import Recipe


def index(request):
    response = dict()
    response['recent'] = Recipe.fetch_all(limit=12, order_by='creation_time')
    return response