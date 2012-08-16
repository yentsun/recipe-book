# -*- coding: utf-8 -*-

from pyramid.httpexceptions import HTTPFound
from kook.models.recipe import Tag, Dish

def index(request):
    return {'dishes': Dish.fetch_all()}

def read(request):
    title = request.matchdict['title']
    dish = Dish.fetch(title)
    response = {'dish':dish}
    return response

def update(request):
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