# -*- coding: utf-8 -*-

import unittest
import transaction

from pyramid import testing
from pyramid.testing import DummyRequest

from kook.models import Recipe, Step, Action, Product, Ingredient, metadata, DBSession

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
            boil = Action(u'отварить')
            mix = Action(u'перемешать')
            recipe.steps = [
                Step(1, recipe.ingredients[0], boil, time_value=30),
                Step(1, recipe.ingredients[1], boil),
                Step(2, recipe.ingredients[0], Action(u'нарезать'), note=u'cut to little pieces'),
                Step(3, recipe.ingredients[0], mix),
                Step(3, recipe.ingredients[1], mix, time_value=10)
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
        self.assertEqual(response['recipe'].title, u'оливье')
        self.assertEqual(response['recipe'].total_amount, 997)
        self.assertEqual(response['recipe'].ingredients[0].product.title, u'картофель')
        self.assertEqual(response['recipe'].ingredients[0].amount, 400)
        self.assertEqual(response['recipe'].ingredients[4].amount, 172)
        self.assertEqual(len(response['recipe'].steps), 5)
        self.assertEqual(len(response['recipe'].phases), 3)
        self.assertEqual(len(response['recipe'].phases[1].ingredients), 2)
        self.assertEqual(response['recipe'].phases[1].ingredients[0].__str__(), u'картофель 400 г')

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
            ('phase_no', '1'),
            ('ingredients', u'свекла, морковь, картофель'),
            ('action', u'отварить'),
            ('time_value', '60'),
            ('note', u'Пока овощи не станут мягкими'),
            ('phase_no', '2'),
            ('ingredients', u'свекла, морковь, картофель'),
            ('action', u'нарезать'),
            ('time_value', ''),
            ('note', u'Мелкими кубиками'),
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
        self.assertEqual(len(recipe.phases), 2)
        self.assertEqual(len(recipe.phases[1].ingredients), 3)
        assert potato_400g in recipe.phases[1].ingredients
        assert potato_400g in recipe.phases[2].ingredients

    def test_recipe_index_view(self):
        from kook.views import recipe_index_view
        request = DummyRequest()
        response = recipe_index_view(request)
        recipes = response['recipes']
        self.assertEqual(len(recipes), 2)