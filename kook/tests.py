# -*- coding: utf-8 -*-

import json
import unittest
import transaction

from copy import copy
from datetime import date
from webob.multidict import MultiDict
from pyramid.testing import DummyRequest, setUp, tearDown
from pyramid.security import Allow
from sqlalchemy import engine_from_config
from pyramid_beaker import set_cache_regions_from_settings
from paste.deploy.loadwsgi import appconfig

from kook.models import (Recipe, Step, Product, Ingredient, metadata,
                         DBSession, Unit, AmountPerUnit, User, Group)
from kook.views import recipe as recipe_, user as user_

sausage = Product(title=u'колбаса вареная')

class TestRecipeViews(unittest.TestCase):
    """
    -----------------
    RECIPE TESTS
    -----------------
    """

    def setUp(self):
        settings = appconfig('config:testing.ini',
                             'main',
                             relative_to='/home/yentsun/www/kook')
        self.config = setUp(settings=settings)
        engine = engine_from_config(settings)
        set_cache_regions_from_settings(settings)
        DBSession.configure(bind=engine)
        metadata.create_all(engine)
        with transaction.manager:
            user1 = User.construct_from_dict({
                'email': 'user1@acme.com',
                'password': '123456'})
            user1.save()
            user2 = User.construct_from_dict({
                'email': 'user2@acme.com',
                'password': '654321'})
            user2.save()
            recipe = Recipe(title=u'оливье',
                            description=u'Один из самых популярных салатов',
                            author=user1)
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
                Step(2, u'картофель и морковь очистить от кожицы',
                     time_value=5),
                Step(3, u'овощи и колбасу нарезать и перемешать, '
                        u'заправляя майонезом', time_value=1),
                Step(4, u'салат украсить веткой петрушки', time_value=0)
            ]
            recipe2 = copy(recipe)
            recipe3 = copy(recipe)
            recipe2.title = u'Оливье 2'
            recipe3.author = user2
            recipe.save()
            recipe2.save()
            recipe3.save()

    def tearDown(self):
        DBSession.remove()
        tearDown()

    def test_recipe_index(self):
        all = Recipe.fetch_all()
        self.assertEqual(3, len(all))

    def test_recipe_view(self):
        request = DummyRequest()
        request.matchdict['title'] = u'оливье'
        author = User.fetch(email='user1@acme.com')
        request.matchdict['author_id'] = author.id
        response = recipe_.read_view(request)
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
            ('title', u'ВинеГрет '),
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
            ('step_text',
             u'свеклу, морковь и картофель отварить, пока овощи'
             u' не станут мягкими'),
            ('time_value', 60),
            ('step_number', '2'),
            ('step_text',
             u'Нарезать свеклу, морковь и картофель мелкими кубиками'),
            ('time_value', 2),
        ))
        user=User.fetch(email='user1@acme.com')
        request = DummyRequest(POST=POST, user=user)
        recipe_.create_view(request)
        recipe = Recipe.fetch(u'винегрет', user.id)
        assert recipe is not None
        self.assertEqual(recipe.title, u'винегрет')
        self.assertEqual(len(recipe.ingredients), 5)
        self.assertEqual([(Allow, user.id, 'update')], recipe.__acl__)
        potato = Product(u'картофель')
        potato_400g = Ingredient(potato, amount=400)
        assert potato in recipe.products
        assert potato_400g in recipe.ingredients
        self.assertEqual(len(recipe.steps), 2)
        self.assertEqual(60, recipe.ordered_steps[1].time_value)

        #testing initial output
        request = DummyRequest()
        response = recipe_.create_view(request)
        assert potato in response['products']

    def test_create_invalid_recipe(self):
        POST = MultiDict((
            ('title', u'Винегрет'),
            ('description', u'Салат винегрет'),
            ('product_title', u''),
            ('amount', ''),
            ('unit_title', u''),
            ('step_number', ''),
            ('step_text', u''),
            ('time_value', 0)
            ))
        request = DummyRequest(POST=POST,
                               user=User.fetch(email='user1@acme.com'))
        recipe_.create_view(request)
        recipe = Recipe.fetch(u'Винегрет', 'user1@acme.com')
        assert recipe is None

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
            ('step_text', u'свеклу, морковь и картофель отварить,'
                          u' пока овощи не станут мягкими'),
            ('time_value', 60),
            ('step_number', 2),
            ('step_text', u'Нарезать свеклу, морковь и картофель'
                          u' мелкими кубиками'),
            ('time_value', 2),
        ))
        request = DummyRequest(POST=POST)
        request.matchdict['title'] = u'оливье'
        request.user = User.fetch(email='user1@acme.com')
        request.matchdict['update_path'] = \
            '/update_recipe/%D0%BE%D0%BB%D0%B8%D0%B2%D1%8C%D0%B5'
        recipe_.update_view(request)
        recipe_old = Recipe.fetch(u'оливье', request.user.id)
        assert recipe_old is None
        recipe_new = Recipe.fetch(u'оливье-3', request.user.id)
        assert recipe_new is not None
        assert sausage not in recipe_new.products
        self.assertEqual(recipe_new.description, u'Салат винегрет')
        self.assertEqual(len(recipe_new.steps), 2)

    def test_delete_recipe_view(self):
        user = User.fetch(email='user1@acme.com')
        request = DummyRequest(user=user)
        all = Recipe.fetch_all()
        request.matchdict['title'] = u'Оливье 2'
        recipe_.delete_view(request)
        self.assertEqual(len(Recipe.fetch_all()), 2)
        self.assertEqual(Recipe.fetch(u'Оливье 2', 'user1@acme.com'), None)

    def test_user_recipe_index_view(self):
        request = DummyRequest(user=User.fetch(email='user1@acme.com'))
        response = recipe_.index_view(request)
        recipes = response['user_recipes']
        self.assertEqual(len(recipes), 2)

    def test_alt_user_recipe_index_view(self):
        request = DummyRequest(user=User.fetch(email='user2@acme.com'))
        response = recipe_.index_view(request)
        recipes = response['user_recipes']
        self.assertEqual(len(recipes), 1)

    def test_product_units_view(self):
        request = DummyRequest()
        request.matchdict['product_title'] = u'картофель'
        response = recipe_.product_units_view(request)
        response = json.dumps(response)
        self.assertEqual('[{"amount": 8000, "abbr": "bkt", "title": "bucket"}, '
                         '{"amount": 100, "abbr": "pcs", "title": "piece"}]',
                         response)

        request.matchdict['product_title'] = u'картофел'
        response = recipe_.product_units_view(request)
        response = json.dumps(response)
        self.assertEqual('[]', response)

    def test_recipe_to_json(self):
        request = DummyRequest()
        request.matchdict['title'] = u'оливье'
        request.matchdict['author_id'] = User.fetch(email='user1@acme.com').id
        response = recipe_.read_view(request)
        recipe = response['recipe']
        recipe_json = json.dumps(recipe.to_dict())
        self.assertEqual('{'
        '"ingredients": '
          '[{"amount": 400,'
           ' "unit_title": "piece", '
            '"product_title": "\u043a\u0430\u0440\u0442\u043e\u0444'
            '\u0435\u043b\u044c"}, '
            '{"amount": 200,'
            ' "unit_title": "", '
             '"product_title": "\u043a\u043e\u043b\u0431\u0430\u0441'
             '\u0430 \u0432\u0430\u0440\u0435\u043d\u0430\u044f"},'
           ' {"amount": 172, "unit_title": "", '
             '"product_title": "\u044f\u0439\u0446\u043e \u043a\u0443'
             '\u0440\u0438\u043d\u043e\u0435"}, '
             '{"amount": 150, "unit_title": "", '
             '"product_title": "\u043c\u043e\u0440\u043a\u043e\u0432'
             '\u044c"}, '
             '{"amount": 75, '
             '"unit_title": "",'
             ' "product_title": "\u043b\u0443\u043a \u0440\u0435'
             '\u043f\u0447\u0430\u0442\u044b\u0439"}], '
             '"steps": [{"text": "\u0432\u0441\u0435 \u043e\u0432\u043e'
             '\u0449\u0438 \u043e\u0442\u0432\u0430\u0440\u0438\u0442'
             '\u044c", "time_value": 30, "number": 1},'
             ' {"text": "\u043a\u0430\u0440\u0442\u043e\u0444\u0435'
             '\u043b\u044c \u0438 \u043c\u043e\u0440\u043a\u043e\u0432'
             '\u044c \u043e\u0447\u0438\u0441\u0442\u0438\u0442\u044c '
             '\u043e\u0442 \u043a\u043e\u0436\u0438\u0446\u044b",'
             ' "time_value": 5, "number": 2},'
             ' {"text": "\u043e\u0432\u043e\u0449\u0438 \u0438 \u043a'
             '\u043e\u043b\u0431\u0430\u0441\u0443 \u043d\u0430\u0440'
             '\u0435\u0437\u0430\u0442\u044c \u0438 \u043f\u0435\u0440'
             '\u0435\u043c\u0435\u0448\u0430\u0442\u044c, \u0437\u0430'
             '\u043f\u0440\u0430\u0432\u043b\u044f\u044f \u043c\u0430'
             '\u0439\u043e\u043d\u0435\u0437\u043e\u043c", '
             '"time_value": 1, "number": 3}, '
             '{"text": "\u0441\u0430\u043b\u0430\u0442 \u0443\u043a'
             '\u0440\u0430\u0441\u0438\u0442\u044c \u0432\u0435\u0442'
             '\u043a\u043e\u0439 \u043f\u0435\u0442\u0440\u0443\u0448'
             '\u043a\u0438", "time_value": 0, "number": 4}], '
             '"description": "\u041e\u0434\u0438\u043d \u0438\u0437 '
             '\u0441\u0430\u043c\u044b\u0445 \u043f\u043e\u043f\u0443'
             '\u043b\u044f\u0440\u043d\u044b\u0445 \u0441\u0430\u043b'
             '\u0430\u0442\u043e\u0432", "title": "\u043e\u043b\u0438'
             '\u0432\u044c\u0435"}', recipe_json)

class TestUserViews(unittest.TestCase):
    """
    ----------
    USER TESTS
    ----------
    """
    def setUp(self):
        settings = appconfig('config:testing.ini',
            'main',
            relative_to='/home/yentsun/www/kook')
        self.config = setUp(settings=settings)
        engine = engine_from_config(settings)
        set_cache_regions_from_settings(settings)
        DBSession.configure(bind=engine)
        metadata.create_all(engine)
        with transaction.manager:
            user1 = User('753f10bd80dc4d2a977749ff12d7232f',
                         'user1@acme.com', User.generate_hash('1234'),
                         [Group('admins'), Group('bosses')])
            user2 = User('8050bc54f47b451ca7ef2c399b31d494',
                         'user2@acme.com', User.generate_hash('gtER'),
                         [Group('workers'), Group('clerks')])
            user3 = User('c8a81b82e75344d0a8adb6dccbea635f',
                         'user3@acme.com', User.generate_hash('0983'))
            user1.save()
            user2.save()
            user3.save()

    def tearDown(self):
        DBSession.remove()
        tearDown()

    def test_register_view(self):
        POST = MultiDict((
            ('email', 'test@acme.com'),
            ('password', u'8Z然y落Σ#2就O'),
            ))
        request = DummyRequest(POST=POST)
        request.matchdict['next_path'] = '/dashboard'
        user_.register_view(request)
        user = User.fetch(email='test@acme.com')
        assert user is not None
        self.assertEqual('f76acb34db8e6def25cd079978e511d1',
                         user.password_hash)
        self.assertEqual('registered', user.groups[0].title)
        group_strings = User.group_finder(user=user)
        assert 'registered' in group_strings
        assert user.profile is not None
        assert type(user.profile.registration_day) is date

    def test_deny_invalid_password(self):
        POST = MultiDict((
            ('email', 'invalid@acme.com'),
            ('password', u'8ZO'),
            ))
        request = DummyRequest(POST=POST)
        request.matchdict['next_path'] = '/dashboard'
        user_.register_view(request)
        user = User.fetch(email='invalid@acme.com')
        assert user is None

    def test_register_existent_user(self):
        POST = MultiDict((
            ('email', 'user1@acme.com'),
            ('password', u'8765432'),
            ))
        request = DummyRequest(POST=POST)
        request.matchdict['next_path'] = '/dashboard'
        user_.register_view(request)
        user = User.fetch(email='user1@acme.com')
        self.assertEqual('930ea67201ae3f808b954e3073c6b7d2',
                         user.password_hash)

    def test_update_profile(self):
        POST = MultiDict((
            ('nickname', 'AcmeBOSS'),
            ('real_name', 'John Darko'),
            ('birthday', '1979-07-21'),
            ('location', 'Europe/London')
        ))
        request = DummyRequest(POST=POST,
                               user=User.fetch(email='user1@acme.com'))
        user_.update_profile_view(request)
        user = User.fetch(email='user1@acme.com')
        self.assertEqual('AcmeBOSS', user.profile.nickname)
        self.assertEqual(date(1979, 7, 21), user.profile.birthday)

    def test_user_groups(self):
        user=User.fetch(email='user1@acme.com')
        user2 = User.fetch(email='user2@acme.com')
        self.assertEqual(2, len(user.groups))
        self.assertEqual(2, len(user2.groups))
        group_strings = User.group_finder(user=user)
        assert u'admins' in group_strings
        assert u'bosses' in group_strings
        assert u'workers' in User.group_finder(user=user2)
        assert u'clerks' in User.group_finder(user=user2)
