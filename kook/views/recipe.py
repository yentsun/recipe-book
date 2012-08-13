# -*- coding: utf-8 -*-

import json

from datetime import datetime
from pyramid.httpexceptions import HTTPFound, HTTPError
from pyramid.security import has_permission, Deny
from pyramid.i18n import get_localizer
from beaker.cache import cache_region, region_invalidate
from kook.models import UPVOTE, DOWNVOTE, UPVOTE_REQUIRED_REP, DOWNVOTE_REQUIRED_REP, form_msg

from kook.models.recipe import Product, Recipe, Tag, Comment, Dish

@cache_region('long_term', 'common')
def common():
    return {'products': Product.fetch_all(),
            'dishes': Dish.fetch_all(),
            'tags': Tag.fetch_all()}

def index_view(request):
    response = dict()
    response['user_recipes'] = Recipe.fetch_all(author_id=request.user.id)
    response['dishes'] = Dish.fetch_all()
    return response

def read_dish(request):
    title = request.matchdict['title']
    dish = Dish.fetch(title)
    response = {'dish':dish}
    return response

def update_dish(request):
    title = request.matchdict['title']
    response = {'tags': Tag.fetch_all()}
    try:
        update_path = request.current_route_url(id=id)
    except ValueError:
        update_path = '/'
    dish = Dish.fetch(title)
    response.update({'update_dish_path': update_path,
                     'dish': dish})
    if request.POST:
        dish.description = request.POST.getone('description')
        tag_titles = request.POST.getall('tag')
        dish.tags = [Tag.fetch(title) for title in tag_titles]
        dish.save()
        request.session.flash(u'<div class="alert alert-success">'
                              u'Блюдо обновлено</div>')
        return HTTPFound(update_path)
    return response

def tag(request):
    title = request.matchdict['title']
    tag = Tag.fetch(title)
    dishes = Dish.fetch_all(tag_title=title)
    response = {'tag':tag, 'dishes':dishes}
    return response

def read_view(request):
    id = request.matchdict['id']
    recipe = Recipe.fetch(id)
    last_vote = None
    try:
        last_vote = request.user.last_vote(recipe.id)
        recipe.attach_acl(get_acl_by_last_vote(request.user, recipe))
    except AttributeError:
        recipe.attach_acl()
    response = {'recipe': recipe,
                'UPVOTE': UPVOTE,
                'DOWNVOTE': DOWNVOTE,
                'last_vote': last_vote,
                'can_comment': has_permission('comment', recipe, request),
                'can_update': has_permission('update', recipe, request),
                'can_upvote': has_permission('upvote', recipe, request),
                'can_downvote': has_permission('downvote', recipe, request)}
    return response

def delete_view(request):
    id = request.matchdict['id']
    recipe = Recipe.fetch(id=id)
    recipe.attach_acl()
    if has_permission('delete', recipe, request):
        recipe.delete()
        request.session.flash(u'<div class="alert">Рецепт "%s" удален!</div>'
                              % recipe.dish.title)
        region_invalidate(common, 'long_term', 'common')
        return HTTPFound('/dashboard?invalidate_cache=true')
    else:
        request.session.flash(u'<div class="alert alert-error">'
                              u'У вас нет прав удалять этот рецепт</div>')
        return HTTPFound('/')

def create_update(request):
    id = None
    if 'id' in request.matchdict:
        id = request.matchdict['id']
    response = common()
    localizer = get_localizer(request)

    try:
        next_path = request.current_route_url(id=id)
    except ValueError:
        next_path = '/'

    if id:
        recipe = Recipe.fetch(id)
        recipe.attach_acl()
        allowed = has_permission('update', recipe, request)
    else:
        recipe = Recipe.dummy(author=request.user)
        allowed = True

    response.update({'update_recipe_path': next_path,
                     'recipe': recipe})

    if request.POST:

        #if json file received
        if 'json_upload' in request.POST:
            input_file = request.POST['file'].file
            input_file.seek(0)
            data = json.load(input_file)
            recipe = Recipe.dummy(author=request.user, dict_=data)
            response['recipe'] = recipe
        #if recipe creation/update received
        else:
            result = Recipe.construct_from_multidict(request.POST, recipe,
                                                 localizer=localizer,
                                                 fetch_dish_image=True)
            if allowed:
                try:
                    if id:
                        recipe.delete()
                        result.update_time = datetime.now()
                    result.save()
                    region_invalidate(common, 'long_term', 'common')
                    request.session.flash(u'<div class="alert alert-success">'
                                      u'Рецепт обновлен!</div>')
                    try:
                        next_path = request.route_url('update_recipe',
                                                   id=result.id)
                    except:
                        pass
                    return HTTPFound(next_path)

                except AttributeError:
                    recipe.revert()
                    request.session.flash(u'<div class="alert alert-error">'
                                        u'Ошибка при обновлении рецепта!'
                                      u'</div>')
                    response['errors'] = json.dumps(result['errors'])
                    response['data'] = result['original_data']
            else:
                request.session.flash(
                    u'<div class="alert alert-error">'
                    u'У вас нет прав на добавление/обновление этого рецепта!</div>'
                )
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
    Process voting from recipe request. Return new recipe rating.
    Ajax only.
    """
    if request.POST:
        id = request.POST.getone('recipe_id')
        vote_value = int(request.POST.getone('vote_value'))
        perm_required = None
        if vote_value is UPVOTE:
            perm_required = 'upvote'
        if vote_value is DOWNVOTE:
            perm_required = 'downvote'
        recipe = Recipe.fetch(id)
        last_vote_acl = get_acl_by_last_vote(request.user, recipe)
        recipe.attach_acl(prepend=last_vote_acl)
        can_do = has_permission(perm_required, recipe, request)
        if can_do:
            recipe.add_vote(request.user, vote_value)
            recipe.save()
            return {'new_rating': recipe.rating,
                    'status': 'ok'}
        else:
            msg = form_msg(can_do)
            return {'status': 'error',
                    'message': msg}

def comment_view(request):
    """
    Process recipe comment request. Return 'ok' or 'error'. Ajax only.

    ACL attachment for comment is skipped because comment author is enforced
    to be the authorized user and for now he can do *whatever* to his comments.
    """
    if request.POST:
        recipe_id = request.POST.getone('recipe_id')
        text = request.POST.getone('comment_text')
        try:
            creation_time = request.POST.getone('creation_time')
        except KeyError:
            creation_time = None

        #if time is present, update
        if creation_time:
            comment = Comment.fetch((request.user.id, recipe_id,
                                     creation_time))
            comment.text = text
            comment.save()

        #otherwise create
        else:
            comment = Comment.construct_from_dict({'text':text}, request.user)
            try:
                recipe = Recipe.fetch(recipe_id)
                recipe.comments.append(comment)
                recipe.save()

            #invalid comment
            except AttributeError:
                raise HTTPError

        return {'comment': comment,
                'can_edit': True}

def delete_comment_view(request):
    recipe_id = request.matchdict['recipe_id']
    creation_time = request.matchdict['creation_time']
    Comment.delete(request.user.id, recipe_id, creation_time)
    return {'status': 'ok'}

def get_acl_by_last_vote(user, recipe):
    acl = []
    last_vote = None
    try:
        last_vote = user.last_vote(recipe.id).value
    except AttributeError:
        pass
    if last_vote is UPVOTE:
        acl = [(Deny, user.id, 'upvote')]
    if last_vote is DOWNVOTE:
        acl = [(Deny, user.id, 'downvote')]
    return acl