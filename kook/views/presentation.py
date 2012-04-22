# -*- coding: utf-8 -*-

from base64 import b64decode
from pyramid.security import authenticated_userid
from ..models import Recipe

def recipe_index_view(request):
    response = dict()
    if 'author_id' in request.matchdict:
        user_id = request.matchdict['author_id']
    else:
        user_id = authenticated_userid(request)
    response['user_recipes'] = Recipe.fetch_all(user_id)
    return response

def read_recipe_view(request):
    response = dict()
    title = request.matchdict['title']
    author_id = request.matchdict['author_id']
    recipe = Recipe.fetch(title=title, author_id=author_id)
    response['recipe'] = recipe
    return response