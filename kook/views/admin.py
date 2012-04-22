# -*- coding: utf-8 -*-
import json
from base64 import b64decode
from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid
from beaker.cache import cache_region, region_invalidate
from ..models import Recipe, Product, User

@cache_region('long_term', 'common')
def common():
    return {'products': Product.fetch_all()}

def create_recipe_view(request):
    response = common()
    response['create_recipe_path'] = '/create_recipe'
    if 'author_id' in request.matchdict:
        author_id = request.matchdict['author_id']
    else:
        author_id = authenticated_userid(request)
    author = User.fetch(id=author_id)
    if request.POST:
        result = Recipe.construct_from_multidict(request.POST)
        if isinstance(result, Recipe):
            result.author = author
            result.save()
            region_invalidate(common, 'long_term', 'common')
            request.session.flash(u'<div class="alert alert-success">' \
                                  u'Рецепт "%s" добавлен!' \
                                  u'</div>'
                                  % result.title)
            return HTTPFound('/?invalidate_cache=true')
        else:
            request.session.flash(u'<div class="alert alert-error">'
                                  u'Ошибка при добавлении рецепта!</div>')
            response['error_data'] = json.dumps(result)
    return response

def delete_recipe_view(request):
    title = request.matchdict['title']
    author_id = request.matchdict['author_id']
    victim_title = Recipe.delete(title, author_id=author_id)
    request.session.flash(u'<div class="alert">Рецепт "%s" удален!</div>' % victim_title)
    region_invalidate(common, 'long_term', 'common')
    return HTTPFound('/?invalidate_cache=true')

def update_recipe_view(request):
    title = request.matchdict['title']
    if 'author_id' in request.matchdict:
        author_id = request.matchdict['author_id']
    else:
        author_id = authenticated_userid(request)
    author = User.fetch(id=author_id)
    response = common()
    if 'update_path' in request.matchdict:
        update_path = request.matchdict['update_path']
    else:
        update_path = request.current_route_url(title=title)
    if request.POST:
        result = Recipe.construct_from_multidict(request.POST)
        if isinstance(result, Recipe):
            result.author = author
            result.update(title, author_id=author_id)
            region_invalidate(common, 'long_term', 'common')
            request.session.flash(u'<div class="alert alert-success">'
                                  u'Рецепт обновлен!</div>')
            return HTTPFound(update_path)
        else:
            request.session.flash(u'<div class="alert alert-error">'
                                  u'Ошибка при обновлении рецепта!</div>')
            response['error_data'] = json.dumps(result)
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

