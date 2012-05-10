# -*- coding: utf-8 -*-

from kook.models.recipe import Recipe, Dish, Tag
from kook.models.user import User

def index_view(request):
    response = dict()
    response['best_recipes'] = Recipe.fetch_all(limit=10)
    response['best_users'] = User.fetch_all()
    response['popular_dishes'] = Dish.fetch_all()
    response['tags'] = Tag.fetch_all()
    return response