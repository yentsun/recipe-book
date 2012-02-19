# -*- coding: utf-8 -*-

from pyramid.httpexceptions import HTTPFound

from .models import Recipe, Step

def recipe_index_view(request):
    recipes = Recipe.fetch_all()
    return {'recipes':recipes}

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

def read_recipe_view(request):
    title = request.matchdict['title']
    recipe = Recipe.fetch(title=title)
    return {'recipe':recipe}

def update_recipe_view(request):
    title = request.matchdict['title']
    update_recipe_path = request.route_url('update_recipe', title=title)
    if request.POST:
        recipe = Recipe.construct_from_multidict(request.POST)
        recipe.update()
        request.session.flash(u'<div class="ok">Рецепт обновлен!</div>')
        return HTTPFound(update_recipe_path)
    else:
        recipe = Recipe.fetch(title)
        return {'update_recipe_path': update_recipe_path,
                'recipe': recipe}