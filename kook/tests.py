# -*- coding: utf-8 -*-
import json
import unittest
import transaction

from pyramid import testing
from pyramid.testing import DummyRequest
from webob.multidict import MultiDict
from sqlalchemy import engine_from_config
from pyramid_beaker import set_cache_regions_from_settings
from paste.deploy.loadwsgi import appconfig

from kook.models import (Recipe, Step, Product, Ingredient, metadata, DBSession,
                         Unit, AmountPerUnit)
from kook.views.presentation import (read_recipe_view,
                                     recipe_index_view)
from kook.views.admin import (create_recipe_view,
                              update_recipe_view,
                              delete_recipe_view,
                              product_units_view)

sausage = Product(title=u'колбаса вареная')

class TestMyViews(unittest.TestCase):
    def setUp(self):
        settings = appconfig('config:testing.ini',
                             'main',
                             relative_to='/home/yentsun/www/kook')
        self.config = testing.setUp(settings=settings)
        engine = engine_from_config(settings)
        set_cache_regions_from_settings(settings)
        DBSession.configure(bind=engine)
        metadata.create_all(engine)
        with transaction.manager:
            recipe = Recipe(title=u'оливье',
                            description=u'Один из самых популярных салатов')
            potato = Product(title=u'картофель')
            piece = Unit(u'piece', u'pcs')
            bucket = Unit(u'bucket', u'bkt')
            onion_piece = Unit(u'луковица')
            potato.APUs = [AmountPerUnit(100, piece),
                           AmountPerUnit(8000, bucket)]
            carrot = Product(title=u'морковь')
            onion = Product(title=u'лук репчатый')
            onion.APUs = [AmountPerUnit(75, onion_piece)]
            egg = Product(title=u'яйцо куриное')
            recipe.ingredients = [
                Ingredient(potato, amount=400, unit=piece),
                Ingredient(carrot, amount=150),
                Ingredient(sausage, amount=200),
                Ingredient(onion, amount=75),
                Ingredient(egg, amount=172)
            ]
            recipe.steps = [
                Step(1, u'все овощи отварить', time_value=30),
                Step(2, u'картофель и морковь очистить от кожицы', time_value=5),
                Step(3, u'овощи и колбасу нарезать и перемешать, заправляя майонезом', time_value=1),
                Step(4, u'салат украсить веткой петрушки', time_value=0)
            ]
            recipe.save()
            recipe2 = recipe
            recipe2.title = u'Оливье 2'
            recipe2.save()

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_recipe_view(self):
        request = DummyRequest()
        request.matchdict['title'] = u'оливье'
        response = read_recipe_view(request)
        recipe = response['recipe']
        potato = Product(title=u'картофель')
        garnishing = Step(4, u'салат украсить веткой петрушки', time_value=0)
        self.assertEqual(recipe.title, u'оливье')
        self.assertEqual(recipe.total_amount, 997)
        assert potato in recipe.products
        self.assertEqual(len(recipe.steps), 4)
        potato_400g = Ingredient(potato, amount=400)
        self.assertEqual(recipe.ingredients[0].apu, 100)
        self.assertEqual(recipe.ingredients[1].apu, 1)
        assert potato_400g in recipe.ingredients
        self.assertEqual(recipe.ingredients[0].measured, 4)
        for ingredient in recipe.ingredients:
            if ingredient.product.title == u'лук':
                self.assertEqual(ingredient.measured, 1)
        assert garnishing in recipe.steps

    def test_create_recipe_view(self):
        #testing post
        POST = MultiDict((
            ('title', u' Винегрет '),
            ('description', u'Салат винегрет'),
            ('product_title', u'свекла'),
            ('amount', '400'),
            ('unit_title', u'штука'),
            ('product_title', u'морковь'),
            ('amount', '300'),
            ('unit_title', ''),
            ('product_title', u'картофель'),
            ('amount', '400'),
            ('unit_title', ''),
            ('product_title', u'квашеная капуста'),
            ('amount', '200'),
            ('unit_title', ''),
            ('product_title', u'лук репчатый'),
            ('amount', '150'),
            ('unit_title', ''),
            ('step_number', '1'),
            ('step_text', u'свеклу, морковь и картофель отварить, пока овощи не станут мягкими'),
            ('time_value', 60),
            ('step_number', '2'),
            ('step_text', u'Нарезать свеклу, морковь и картофель мелкими кубиками'),
            ('time_value', 2),
        ))
        request = DummyRequest(POST=POST)
        create_recipe_view(request)
        recipe = Recipe.fetch(u'винегрет')
        assert recipe is not None
        self.assertEqual(recipe.title, u'винегрет')
        self.assertEqual(len(recipe.ingredients), 5)
        potato = Product(u'картофель')
        potato_400g = Ingredient(potato, amount=400)
        assert potato in recipe.products
        assert potato_400g in recipe.ingredients
        self.assertEqual(len(recipe.steps), 2)
        self.assertEqual(60, recipe.ordered_steps['1'].time_value)

        #testing initial output
        request = DummyRequest()
        response = create_recipe_view(request)
        assert potato in response['products']

    def test_update_recipe_view(self):
        POST = MultiDict((
            ('title', u'оливье-3'),
            ('description', u'Салат винегрет'),
            ('product_title', u'свекла'),
            ('amount', '400'),
            ('product_title', u'морковь'),
            ('amount', '300'),
            ('product_title', u'картофель'),
            ('amount', '400'),
            ('product_title', u'квашеная капуста'),
            ('amount', '200'),
            ('product_title', u'лук репчатый'),
            ('amount', '150'),
            ('step_number', '1'),
            ('step_text', u'свеклу, морковь и картофель отварить, пока овощи не станут мягкими'),
            ('time_value', 60),
            ('step_number', 2),
            ('step_text', u'Нарезать свеклу, морковь и картофель мелкими кубиками'),
            ('time_value', 2),
        ))
        request = DummyRequest(POST=POST)
        request.matchdict['title'] = u'оливье'
        request.matchdict['update_path'] = \
            '/update_recipe/%D0%BE%D0%BB%D0%B8%D0%B2%D1%8C%D0%B5'
        update_recipe_view(request)
        recipe_old = Recipe.fetch(u'оливье')
        assert recipe_old is None
        recipe_new = Recipe.fetch(u'оливье-3')
        assert recipe_new is not None
        assert sausage not in recipe_new.products
        self.assertEqual(recipe_new.description, u'Салат винегрет')
        self.assertEqual(len(recipe_new.steps), 2)

        #testing initial output
        request = DummyRequest()
        response = create_recipe_view(request)
        potato = Product(u'картофель')
        assert potato in response['products']

    def test_delete_recipe_view(self):
        request = DummyRequest()
        request.matchdict['title'] = u'Оливье 2'
        response = delete_recipe_view(request)
        self.assertEqual(len(Recipe.fetch_all()), 1)
        self.assertEqual(Recipe.fetch(u'Оливье 2'), None)

    def test_recipe_index_view(self):
        request = DummyRequest()
        response = recipe_index_view(request)
        recipes = response['recipes']
        self.assertEqual(len(recipes), 2)

    def test_product_units_view(self):
        request = DummyRequest()
        request.matchdict['product_title'] = u'картофель'
        response = product_units_view(request)
        response = json.dumps(response)
        self.assertEqual('[{"amount": 8000, "abbr": "bkt", "title": "bucket"}, {"amount": 100, "abbr": "pcs", "title": "piece"}]', response)

        request.matchdict['product_title'] = u'картофел'
        response = product_units_view(request)
        response = json.dumps(response)
        self.assertEqual('[]', response)