# -*- coding: utf-8 -*-

import json

from datetime import datetime
from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission
from pyramid.i18n import get_localizer
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
#    locale = Locale(get_locale_name(request))
#    print '---------------'
#    print format_date(datetime.datetime.now(), format=u'EEE, MMM d, yyyy',
#                      locale=locale)
#    from pyramid.i18n import TranslationString
#    req = TranslationString('Required')
#    print '------------------------------------'
#    print localizer.translate(req, domain='colander')
#    print localizer.locale_name
#    print req
    response = common()
    localizer = get_localizer(request)
    response['create_recipe_path'] = '/create_recipe'
    response['data'] = None
    if request.POST:
        result = Recipe.construct_from_multidict(request.POST,
                                                 localizer=localizer)
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
            response['errors'] = json.dumps(result['errors'])
            response['data'] = result['original_data']
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
    localizer = get_localizer(request)
    try:
        update_path = request.current_route_url(id=id)
    except ValueError:
        update_path = '/'
    recipe = Recipe.fetch(id)
    response.update({'update_recipe_path': update_path,
                     'recipe': recipe})
    if request.POST:
        result = Recipe.construct_from_multidict(request.POST,
                                                 localizer=localizer)
        if isinstance(result, Recipe):
            if has_permission('update', recipe, request):
                result.id = recipe.id
                result.author = recipe.author
                result.id = recipe.id
                result.creation_time = recipe.creation_time
                result.update_time = datetime.now()
                recipe.delete()
                result.save()
                region_invalidate(common, 'long_term', 'common')
                request.session.flash(u'<div class="alert alert-success">'
                                      u'Рецепт обновлен!</div>')
                return HTTPFound(update_path)
        else:
            request.session.flash(u'<div class="alert alert-error">'
                                  u'Ошибка при обновлении рецепта!</div>')
            response['errors'] = json.dumps(result['errors'])
            response['data'] = result['original_data']
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
    id = request.matchdict['id']
    recipe = Recipe.fetch(id)
    if request.POST:
        new_status_id = request.POST.getone('new_status')
        recipe.status_id = int(new_status_id)
        recipe.save()
        return {'status_id': new_status_id}

def vote_view(request):
    """
    Process voting fro recipe request. Return new recipe rating.
    Ajax only.
    """
    if request.POST:
        id = request.POST.getone('recipe_id')
        vote_value = int(request.POST.getone('vote_value'))
        recipe = Recipe.fetch(id)
        recipe.add_vote(request.user, vote_value)
        recipe.save()
        return {'new_rating': recipe.rating}

def add_comment_view(request):
    """
    Process recipe comment request. Return 'ok' or 'error'
    Ajax only.
    """
    if request.POST:
        id = request.POST.getone('recipe_id')
        text = request.POST.getone('text')
        recipe = Recipe.fetch(id)
        recipe.add_comment(request.user, text)
        recipe.save()
        return {'status': 'ok'}
