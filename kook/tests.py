# -*- coding: utf-8 -*-

import unittest
import transaction

from pyramid import testing
from pyramid.testing import DummyRequest

from kook.models import Recipe, Step, Product, Ingredient, metadata, DBSession

class TestMyViews(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        DBSession.configure(bind=engine)
        metadata.create_all(engine)
        with transaction.manager:
            recipe = Recipe(title=u'оливье',
                            description=u'Один из самых популярных салатов')
            potato = Product(title=u'картофель')
            carrot = Product(title=u'морковь')
            sausage = Product(title=u'колбаса вареная')
            onion = Product(title=u'лук репчатый')
            egg = Product(title=u'яйцо куриное')
            recipe.ingredients = [
                Ingredient(potato, amount=400),
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
        from kook.views import recipe_view
        request = DummyRequest()
        request.matchdict['title'] = u'оливье'
        response = recipe_view(request)
        recipe = response['recipe']
        potato = Product(title=u'картофель')
        garnishing = Step(4, u'салат украсить веткой петрушки', time_value=0)
        self.assertEqual(recipe.title, u'оливье')
        self.assertEqual(recipe.total_amount, 997)
        assert potato in recipe.products
        self.assertEqual(len(recipe.steps), 4)
        assert garnishing in recipe.steps

    def test_add_recipe_view(self):
        from kook.views import add_recipe_view
        from webob.multidict import MultiDict
        POST = MultiDict((
            ('title', u'Винегрет'),
            ('description', u'Салат винегрет'),
            ('product', u'свекла'),
            ('amount', '400'),
            ('product', u'морковь'),
            ('amount', '300'),
            ('product', u'картофель'),
            ('amount', '400'),
            ('product', u'квашеная капуста'),
            ('amount', '200'),
            ('product', u'лук репчатый'),
            ('amount', '150'),
            ('step_number', '1'),
            ('step_text', u'свеклу, морковь и картофель отварить, пока овощи не станут мягкими'),
            ('time_value', 60),
            ('step_number', 2),
            ('step_text', u'Нарезать свеклу, морковь и картофель мелкими кубиками'),
            ('time_value', 2),
        ))
        request = DummyRequest(POST=POST)
        response = add_recipe_view(request)
        recipe = Recipe.fetch(u'Винегрет')
        assert recipe is not None
        self.assertEqual(recipe.title, u'Винегрет')
        self.assertEqual(len(recipe.ingredients), 5)
        potato = Product(u'картофель')
        potato_400g = Ingredient(potato, 400)
        assert potato in recipe.products
        assert potato_400g in recipe.ingredients
        self.assertEqual(len(recipe.steps), 2)
        self.assertEqual(recipe.ordered_steps[1].time_value, 60)

    def test_recipe_index_view(self):
        from kook.views import recipe_index_view
        request = DummyRequest()
        response = recipe_index_view(request)
        recipes = response['recipes']
        self.assertEqual(len(recipes), 2)