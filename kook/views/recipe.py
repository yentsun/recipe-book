# -*- coding: utf-8 -*-

import json
from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission
from beaker.cache import cache_region, region_invalidate
from kook.models.recipe import Product, Recipe, Tag

@cache_region('long_term', 'common')
def common():
    return {'products': Product.fetch_all(),
            'tags': Tag.fetch_all()}

def index_view(request):
    response = dict()
    response['all_recipes'] = Recipe.fetch_all()
    response['user_recipes'] = Recipe.fetch_all(author_id=request.user.id)
    return response

def read_view(request):
    response = dict()
    id = request.matchdict['id']
    recipe = Recipe.fetch(id)
    response['recipe'] = recipe
    return response

def create_view(request):
    response = common()
    response['create_recipe_path'] = '/create_recipe'
    if request.POST:
        result = Recipe.construct_from_multidict(request.POST)
        if isinstance(result, Recipe):
            result.author = request.user
            result.save()
            region_invalidate(common, 'long_term', 'common')
            request.session.flash(u'<div class="alert alert-success">'\
                                  u'Рецепт "%s" добавлен!'\
                                  u'</div>' % result.dish.title)
            return HTTPFound('/?invalidate_cache=true')
        else:
            request.session.flash(u'<div class="alert alert-error">'
                                  u'Ошибка при добавлении рецепта!</div>')
            response['error_data'] = json.dumps(result)
    return response

def delete_view(request):
    id = request.matchdict['id']
    recipe = Recipe.fetch(id=id)
    if has_permission('delete', recipe, request):
        recipe.delete()
        request.session.flash(u'<div class="alert">Рецепт "%s" удален!</div>'
                              % recipe.dish.title)
        region_invalidate(common, 'long_term', 'common')
        return HTTPFound('/?invalidate_cache=true')

def update_view(request):
    id = request.matchdict['id']
    response = common()
    try:
        update_path = request.current_route_url(id=id)
    except ValueError:
        update_path = '/'
    recipe = Recipe.fetch(id)
    response.update({'update_recipe_path': update_path,
                     'recipe': recipe})
    if request.POST:
        result = Recipe.construct_from_multidict(request.POST)
        if isinstance(result, Recipe):
            if has_permission('update', recipe, request):
                result.id = recipe.id
                result.author = recipe.author
                recipe.delete()
                result.save()
                region_invalidate(common, 'long_term', 'common')
                request.session.flash(u'<div class="alert alert-success">'
                                      u'Рецепт обновлен!</div>')
                return HTTPFound(update_path)
        else:
            request.session.flash(u'<div class="alert alert-error">'
                                  u'Ошибка при обновлении рецепта!</div>')
            response['error_data'] = json.dumps(result)
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

def update_status_view(request):
    title = request.matchdict['title']
    recipe = Recipe.fetch(title, request.user.id)
    if request.POST:
        new_status_id = request.POST.getone('new_status')
        recipe.status_id = new_status_id
        recipe.save()
        return {'status_id': new_status_id}