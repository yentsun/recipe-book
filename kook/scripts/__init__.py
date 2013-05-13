# -*- coding: utf-8 -*-

import os
import codecs
import transaction

from kook.models.sqla_metadata import metadata
from kook.models.recipe import *
from kook.models.user import *


def populate_dummy_data(engine):

    #add users
    metadata.create_all(engine)
    with transaction.manager:
        user1 = User.construct_from_dict({'email': 'user1@acme.com',
                                          'password': u'题GZG例没%07Z'})
        user1.groups = [Group('admins'), Group('upvoters'),
                        Group('registered')]
        user1.favourite_dishes = [Dish(u'potato salad')]
        user1.add_rep(120, 'test')
        user1.save()
        user2 = User.construct_from_dict({
            'email': 'user2@acme.com',
            'password': u'R52RO圣ṪF特J'})
        user2.add_rep(10, 'test')
        user2.groups = [Group('upvoters'), Group('registered')]
        user2.profile = Profile(nickname=u'Butters',
                                real_name=u'Leopold Stotch')
        user2.save()

        #add products with APUs
        potato = Product(title=u'potato')
        batata = Product(title=u'batata')
        piece = Unit(u'piece', u'pcs.')
        bucket = Unit(u'bucket', u'bkt.')
        potato.APUs = [AmountPerUnit(100, piece),
                       AmountPerUnit(8000, bucket)]
        carrot = Product(title=u'carrot')
        onion = Product(title=u'onion')
        potato.save()
        batata.save()
        onion.save()
        carrot.save()

        #add recipes
        _here = os.path.dirname(__file__)
        json_data = codecs.open(os.path.join(_here, 'dummy_recipes.json'), 'r',
                                'utf-8')
        dummy_recipes = json.load(json_data)
        for recipe_dict in dummy_recipes:
            recipe = Recipe.dummy(author=User.fetch(
                email=recipe_dict['author_email']))
            recipe = Recipe.construct_from_dict(recipe_dict, recipe,
                                                fetch_dish_image=False)
            try:
                recipe.save()
            except AttributeError:
                print recipe

        #add dishes
        potato_salad = Dish(u'potato salad')
        potato_salad.tags = [Tag(u'salad'), Tag(u'western')]
        potato_salad.image = DishImage(u'http://simplyrecipes.com/photos/'
                                       u'potato-salad-new.jpg',
                                       u'simplyrecipes.com')
        potato_salad.save()