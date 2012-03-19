# -*- coding: utf-8 -*-

from pyramid.httpexceptions import HTTPFound
from beaker.cache import cache_region, region_invalidate
from ..models import Recipe, Product

@cache_region('long_term', 'common')
def common():
    return {'recipes': Recipe.fetch_all(),
            'products': Product.fetch_all()}

def create_recipe_view(request):
    create_recipe_path = '/create_recipe'
    #   create_recipe_path = request.route_path('add_recipe') TODO tests cause "ComponentLookupError: (<InterfaceClass pyramid.interfaces.IRoutesMapper>, u'')"
    if request.POST:
        recipe = Recipe.construct_from_multidict(request.POST)
        recipe.save()
        region_invalidate(common, 'long_term', 'common')
        request.session.flash(u'<div class="ok">Рецепт добавлен!</div>')
        return HTTPFound('/?invalidate_cache=true')
    else:
        response = common()
        response['create_recipe_path'] = create_recipe_path
        return response

def delete_recipe_view(request):
    title = request.matchdict['title']
    victim_title = Recipe.delete(title)
    request.session.flash(u'<div class="notice">Рецепт "%s" удален!</div>' % victim_title)
    region_invalidate(common, 'long_term', 'common')
    return HTTPFound('/?invalidate_cache=true')

def update_recipe_view(request):
    title = request.matchdict['title']
    if 'update_path' in request.matchdict:
        update_path = request.matchdict['update_path']
    else:
        update_path = request.current_route_url(title=title)
    if request.POST:
        recipe = Recipe.construct_from_multidict(request.POST)
        recipe.update()
        request.session.flash(u'<div class="ok">Рецепт обновлен!</div>')
        return HTTPFound(update_path)
    else:
        response = common()
        response.update({'update_recipe_path': update_path,
                         'recipe': Recipe.fetch(title)})
        return response