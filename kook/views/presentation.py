# -*- coding: utf-8 -*-

from beaker.cache import cache_region
from ..models import Recipe

@cache_region('long_term')
def common():
    return {'recipes': Recipe.fetch_all()}

def recipe_index_view(request):
    return common()

def read_recipe_view(request):
    title = request.matchdict['title']
    recipe = Recipe.fetch(title=title)
    response = common()
    response['recipe'] = recipe
    return response