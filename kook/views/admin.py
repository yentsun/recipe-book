# -*- coding: utf-8 -*-

import json
from pyramid.httpexceptions import HTTPFound
from beaker.cache import cache_region, region_invalidate
from ..models import Recipe, Product, Step, Ingredient

@cache_region('long_term', 'common')
def common():
    return {'recipes': Recipe.fetch_all(),
            'products': Product.fetch_all()}

def create_recipe_view(request):
    create_recipe_path = '/create_recipe'
    response = common()
    #   create_recipe_path = request.route_path('add_recipe') TODO tests cause "ComponentLookupError: (<InterfaceClass pyramid.interfaces.IRoutesMapper>, u'')"
    if request.POST:
        result = Recipe.construct_from_multidict(request.POST)
        if isinstance(result, Recipe):
            result.save()
            region_invalidate(common, 'long_term', 'common')
            request.session.flash(u'<div class="alert alert-success">' \
                                  u'Рецепт "%s" добавлен!' \
                                  u'</div>'
                                  % result.title)
            return HTTPFound('/?invalidate_cache=true')
        else:
            request.session.flash(u'<div class="alert alert-error">'
                                  u'Ошибка при добавлении рецепта!'
                                  u'</div><div class="json_data">%s</div>'
                                  % json.dumps(result))
            return HTTPFound(create_recipe_path)
    else:
        response['create_recipe_path'] = create_recipe_path
        response['step'] = Step.dummy()
        response['ingredient'] = Ingredient.dummy()
        return response

def delete_recipe_view(request):
    title = request.matchdict['title']
    victim_title = Recipe.delete(title)
    request.session.flash(u'<div class="alert">Рецепт "%s" удален!</div>' % victim_title)
    region_invalidate(common, 'long_term', 'common')
    return HTTPFound('/?invalidate_cache=true')

def update_recipe_view(request):
    title = request.matchdict['title']
    if 'update_path' in request.matchdict:
        update_path = request.matchdict['update_path']
    else:
        update_path = request.current_route_url(title=title)
    if request.POST:
        result = Recipe.construct_from_multidict(request.POST)
        if isinstance(result, Recipe):
            result.update(title)
            if 'update_path' not in request.matchdict: #this check is only for tests
                update_path = request.current_route_url(title=result.title)
            region_invalidate(common, 'long_term', 'common')
            request.session.flash(u'<div class="alert alert-success">Рецепт обновлен!</div>')
        else:
            request.session.flash(u'<div class="alert alert-error">'
                                  u'Ошибка при обновлении рецепта!'
                                  u'<div class="json-data">%s</div></div>'
                                  % json.dumps(result))
        return HTTPFound(update_path)
    else:
        response = common()
        response.update({'update_recipe_path': update_path,
                         'recipe': Recipe.fetch(title)})
        return response

def product_units_view(request):
    product_title = request.matchdict['product_title']
    product = Product.fetch(product_title)
    result = []
    if product is not None:
        for apu in product.APUs:
            result.append({
                'title': apu.unit.title,
                'abbr': apu.unit.abbr,
                'amount': apu.amount
            })
    return result