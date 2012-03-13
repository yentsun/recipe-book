# -*- coding: utf-8 -*-

from beaker.cache import cache_region, region_invalidate
from ..models import Recipe

@cache_region('long_term', 'common')
def common():
    return {'recipes': Recipe.fetch_all()}

def recipe_index_view(request):
    if 'invalidate_cache' in request.GET:
        region_invalidate(common, 'long_term', 'common')
        print('like invalidated')
    return common()

def read_recipe_view(request):
    title = request.matchdict['title']
    recipe = Recipe.fetch(title=title)
    response = common()
    response['recipe'] = recipe
    return response