# -*- coding: utf-8 -*-

from pyramid.httpexceptions import HTTPFound
from ..models import Recipe

def create_recipe_view(request):
    create_recipe_path = '/create_recipe'
    #   create_recipe_path = request.route_path('add_recipe') TODO tests cause "ComponentLookupError: (<InterfaceClass pyramid.interfaces.IRoutesMapper>, u'')"
    if request.POST:
        recipe = Recipe.construct_from_multidict(request.POST)
        recipe.save()
        request.session.flash(u'<div class="ok">Рецепт добавлен!</div>')
        return HTTPFound(create_recipe_path)
    else:
        return {'create_recipe_path':create_recipe_path}

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
        recipe = Recipe.fetch(title)
        return {'update_recipe_path': update_path,
                'recipe': recipe}