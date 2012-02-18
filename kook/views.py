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
        data = request.POST
        products = data.getall('product')
        amounts = data.getall('amount')
        steps_numbers = data.getall('step_number')
        time_values = data.getall('time_value')
        steps_texts = data.getall('step_text')
        recipe = Recipe(data.getone('title'),
                        data.getone('description'),
                        products_amounts=zip(products, amounts))
        recipe.steps = []
        for number, \
            text,\
            time_value,\
        in zip(steps_numbers,
               steps_texts,
               time_values):
            step = Step(number, text, time_value)
            recipe.steps.append(step)
        recipe.save()
        request.session.flash(u'<div class="ok">Рецепт добавлен!</div>')
        return HTTPFound(create_recipe_path)
    return {'create_recipe_path':create_recipe_path}

def read_recipe_view(request):
    title = request.matchdict['title']
    recipe = Recipe.fetch(title=title)
    return {'recipe':recipe}

def update_recipe_view(request):  #TODO write the template!
    update_recipe_path = '/update_recipe'
    if request.POST:
        data = request.POST
        products = data.getall('product') #TODO organize into function
        amounts = data.getall('amount')
        steps_numbers = data.getall('step_number')
        time_values = data.getall('time_value')
        steps_texts = data.getall('step_text')
        recipe = Recipe(data.getone('title'),
            data.getone('description'),
            products_amounts=zip(products, amounts))
        recipe.steps = []
        for number,\
            text,\
            time_value,\
        in zip(steps_numbers,
            steps_texts,
            time_values):
            step = Step(number, text, time_value)
            recipe.steps.append(step)
        recipe.update()
        request.session.flash(u'<div class="ok">Рецепт обновлен!</div>')
        return HTTPFound(update_recipe_path)
    return {'update_recipe_path':update_recipe_path}