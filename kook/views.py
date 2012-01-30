# -*- coding: utf-8 -*-

from pyramid.httpexceptions import HTTPFound

from .models import Recipe, Step, Action

def recipe_view(request):
    title = request.matchdict['title']
    recipe = Recipe.fetch(title=title)
    return {'recipe':recipe}

def recipe_index_view(request):
    recipes = Recipe.fetch_all()
    return {'recipes':recipes}

def add_recipe_view(request):
    add_recipe_path = '/add_recipe'
#    add_recipe_path = request.route_path('add_recipe') TODO tests cause "ComponentLookupError: (<InterfaceClass pyramid.interfaces.IRoutesMapper>, u'')"
    if request.POST:
        data = request.POST
        products = data.getall('product')
        amounts = data.getall('amount')
        phase_nos = data.getall('phase_no')
        ingredients = data.getall('ingredients')
        actions = data.getall('action')
        time_values = data.getall('time_value')
        notes = data.getall('note')
        recipe = Recipe(data.getone('title'), data.getone('description'), products_amounts=zip(products, amounts))
        recipe.steps = []
        for phase_no, \
            ingredients_,\
            action_title,\
            time_value,\
            note \
        in zip(phase_nos,
            ingredients,
            actions,
            time_values,
            notes):
            for product_title in ingredients_.split(u', '):
                ingredient = recipe.get_ingredient_by_product_title(product_title)
                action = Action(action_title)
                step = Step(phase_no, ingredient, action, time_value, note)
                recipe.steps.append(step)
        recipe.save()
        request.session.flash(u'<div class="ok">Страница обновлена!</div>')
        return HTTPFound(add_recipe_path)
    return {'add_recipe_path':add_recipe_path}

