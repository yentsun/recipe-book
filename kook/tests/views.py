# -*- coding: utf-8 -*-

import os
import json
import unittest
import transaction

from datetime import date, datetime
from webob.multidict import MultiDict
from pyramid.testing import DummyRequest, setUp, tearDown
from pyramid.security import Everyone, Allow, ALL_PERMISSIONS
from sqlalchemy import engine_from_config
from pyramid_beaker import set_cache_regions_from_settings
from paste.deploy.loadwsgi import appconfig
from kook.mako_filters import failsafe_get

from kook.models import DBSession
from kook.models.recipe import (Recipe, Step, Product, Ingredient,
                                Unit, AmountPerUnit, Dish, Tag)
from kook.models.user import User, Group, Profile, RepRecord
from kook.models.sqla_metadata import metadata
from kook.views.recipe import (create_view, delete_view, index_view,
                               read_view, product_units_view, update_view,
                               update_status_view, vote_view, add_comment_view)
from kook.views.user import register_view, update_profile_view

def populate_test_data():

    #add users

    user1 = User.construct_from_dict({
        'email': 'user1@acme.com',
        'password': u'题GZG例没%07Z'})
    user1.groups = [Group('admins'), Group('bosses')]
    user1.favourite_dishes = [Dish(u'potato salad')]
    user1.profile = Profile(rep=100)
    user1.save()
    user2 = User.construct_from_dict({
        'email': 'user2@acme.com',
        'password': u'R52RO圣ṪF特J'})
    user2.groups = [Group('workers'), Group('clerks')]
    user2.profile = Profile(rep=-10)
    user2.save()

    #add products with APUs

    potato = Product(title=u'potato')
    piece = Unit(u'piece', u'pcs.')
    bucket = Unit(u'bucket', u'bkt.')
    potato.APUs = [AmountPerUnit(100, piece),
                   AmountPerUnit(8000, bucket)]
    carrot = Product(title=u'carrot')
    onion = Product(title=u'onion')
    potato.save()
    onion.save()
    carrot.save()

    #add recipes

    _here = os.path.dirname(__file__)
    json_data=open(os.path.join(_here, 'dummy_recipes.json'))
    dummy_recipes = json.load(json_data)
    for num, recipe_dict in enumerate(dummy_recipes):
        recipe = Recipe.construct_from_dict(recipe_dict)
        if isinstance(recipe, Recipe):
            recipe.author = user1
            if num is 2:
                recipe.author = user2
            recipe.save()
        else:
            print recipe

    #add dishes

    potato_salad = Dish(u'potato salad')
    potato_salad.tags = [Tag(u'salad'), Tag(u'western')]
    potato_salad.save()

class TestRecipeViews(unittest.TestCase):

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
            populate_test_data()

    def tearDown(self):
        DBSession.remove()
        tearDown()

    def test_dish(self):
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        potato_salad = Dish.fetch(u'potato salad')
        assert potato_salad
        assert Tag(u'salad') in potato_salad.tags
        assert recipe in potato_salad.recipes

    def test_recipe_index(self):
        all = Recipe.fetch_all()
        self.assertEqual(3, len(all))

    def test_recipe_view(self):
        request = DummyRequest()
        recipe_to_test = Recipe.fetch_all(
            dish_title=u'potato salad')[0]
        request.matchdict['id'] = recipe_to_test.id
        response = read_view(request)
        recipe = response['recipe']
        potato = Product(title=u'potato')
        mix = Step(3, u'Just before serving, add scallions and mint to the '
                      u'salad and toss gently.', time_value=5)
        self.assertEqual(recipe.dish_title, u'potato salad')
        self.assertEqual(recipe.total_amount, 370)
        assert potato in recipe.products
        self.assertEqual(len(recipe.steps), 3)
        potato_300g = Ingredient(potato, amount=300)
        self.assertEqual(recipe.ingredients[0].apu, 100)
        self.assertEqual(recipe.ingredients[1].apu, 1)
        assert potato_300g in recipe.ingredients
        self.assertEqual(recipe.ingredients[0].measured, 3)
        for ingredient in recipe.ingredients:
            if ingredient.product.title == u'лук':
                self.assertEqual(ingredient.measured, 1)
        assert mix in recipe.steps
        self.assertEqual(datetime(2012, 5, 3), recipe.creation_time)

    def test_create_recipe_view(self):
        #testing post
        POST = MultiDict((
            ('dish_title', u'Сельдь под шубой '),
            ('description', u''),
            ('product_title', u'свекла'),
            ('amount', '400'),
            ('unit_title', u'штука'),
            ('product_title', u'морковь'),
            ('amount', '300'),
            ('unit_title', ''),
            ('product_title', u'картофель'),
            ('amount', '400'),
            ('unit_title', ''),
            ('product_title', u'сельдь'),
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
            ('time_value', 2)
        ))
        user=User.fetch(email='user1@acme.com')
        request = DummyRequest(POST=POST, user=user)
        create_view(request)
        recipes = Recipe.fetch_all(dish_title=u'сельдь под шубой')
        assert len(recipes) is not 0
        self.assertEqual(recipes[0].dish.title, u'сельдь под шубой')
        self.assertEqual(len(recipes[0].ingredients), 5)
        self.assertEqual([(Allow, user.id, ALL_PERMISSIONS),
                          (Allow, Everyone, 'read')], recipes[0].__acl__)
        potato = Product(u'картофель')
        potato_400g = Ingredient(potato, amount=400)
        assert potato in recipes[0].products
        assert potato_400g in recipes[0].ingredients
        self.assertEqual(len(recipes[0].steps), 2)
        self.assertEqual(60, recipes[0].ordered_steps[1].time_value)

        #testing initial output

        request = DummyRequest()
        response = create_view(request)
        assert potato in response['products']

    def test_create_invalid_recipe(self):
        POST = MultiDict((
            ('dish_title', u'Уникальное блюдо'),
            ('description', u'его нигде нет!'),
            ('product_title', u''),
            ('amount', ''),
            ('unit_title', u''),
            ('step_number', ''),
            ('step_text', u''),
            ('time_value', 0)
            ))
        request = DummyRequest(POST=POST,
                               user=User.fetch(email='user1@acme.com'))
        create_view(request)
        assert len(Recipe.fetch_all(dish_title=u'Уникальное блюдо')) is 0

    def test_update_recipe_view(self):
        POST = MultiDict((
            ('dish_title', u'Spicy Chick Pee'),
            ('description', u'A not-so-good fall-back meal'),
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
            ('step_text', u'свеклу, морковь и картофель отварить, '
                          u'пока овощи не станут мягкими'),
            ('time_value', 60),
            ('step_number', 2),
            ('step_text', u'Нарезать свеклу, морковь и картофель '
                          u'мелкими кубиками'),
            ('time_value', 2),
        ))
        request = DummyRequest(POST=POST)
        recipe_to_update = Recipe.fetch_all(dish_title=u'spicy chick pea')[0]
        request.matchdict['id'] = recipe_to_update.id
        update_view(request)
        assert len(Recipe.fetch_all(dish_title=u'spicy chick pea')) is 0
        recipe_new = Recipe.fetch_all(dish_title=u'spicy chick pee')[0]
        assert recipe_new is not None
        self.assertEqual(recipe_new.description,
                         u'A not-so-good fall-back meal')
        self.assertEqual(len(recipe_new.steps), 2)
        datetime_format = '%Y-%m-%d %H:%M'
        self.assertEqual(datetime.now().strftime(datetime_format),
                         recipe_new.update_time.strftime(datetime_format))

    def test_delete_recipe_view(self):
        user = User.fetch(email='user1@acme.com')
        recipe_to_delete = Recipe.fetch_all(dish_title=u'potato salad',
                                            author_id=user.id)[0]
        request = DummyRequest(user=user)
        request.matchdict['id'] = recipe_to_delete.id
        delete_view(request)
        self.assertEqual(len(Recipe.fetch_all()), 2)
        assert len(Recipe.fetch_all(dish_title=u'винегрет',
                                    author_id=user.id)) is 0

    def test_user_recipe_index_view(self):
        request = DummyRequest(user=User.fetch(email='user1@acme.com'))
        response = index_view(request)
        recipes = response['user_recipes']
        self.assertEqual(len(recipes), 2)

    def test_alt_user_recipe_index_view(self):
        request = DummyRequest(user=User.fetch(email='user2@acme.com'))
        response = index_view(request)
        recipes = response['user_recipes']
        self.assertEqual(len(recipes), 1)

    def test_product_units_view(self):
        request = DummyRequest()
        request.matchdict['product_title'] = u'potato'
        response = product_units_view(request)
        response = json.dumps(response)
        self.assertEqual(
            '[{"amount": 8000, "abbr": "bkt.", "title": "bucket"}, '
            '{"amount": 100, "abbr": "pcs.", "title": "piece"}]', response)

        request.matchdict['product_title'] = u'batato'
        response = product_units_view(request)
        response = json.dumps(response)
        self.assertEqual('[]', response)

    def test_recipe_to_json(self):
        request = DummyRequest()
        recipe_to_test = Recipe.fetch_all(
            dish_title=u'potato salad',
            author_id=User.fetch(email='user1@acme.com').id)[0]
        request.matchdict['id'] = recipe_to_test.id
        response = read_view(request)
        recipe = response['recipe']
        recipe_json = json.dumps(recipe.to_dict())
        self.assertEqual(
            '{"ingredients": [{"amount": 300, "unit_title": "piece", '
            '"product_title": "potato"}, {"amount": 40, "unit_title": "", '
            '"product_title": "lemon juice"}, {"amount": 30, "unit_title": "", '
            '"product_title": "olive oil (extra virgin)"}], '
            '"steps": [{"text": "Place potatoes in a large saucepan or '
            'Dutch oven and cover with lightly salted water. Bring to a boil '
            'and cook until tender", '
            '"time_value": 30, "number": 1}, {"text": "Whisk lemon juice, oil, '
            'salt and pepper in a large bowl. Add the potatoes and toss to '
            'coat.", "time_value": 1, "number": 2}, '
            '{"text": "Just before serving, add scallions and mint to the '
            'salad and toss gently.", "time_value": 5, "number": 3}], '
            '"dish_title": "potato salad", '
            '"description": "The **fastest** way to cook potato salad"}',
            recipe_json)

    def test_recipe_acl(self):
        user = User.fetch(email='user1@acme.com')
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        assert (Allow, user.id, ALL_PERMISSIONS) in recipe.__acl__

    def test_failsafe_get(self):
        none = None
        res0 = failsafe_get(none, 'dish_title')
        self.assertEqual('', res0)
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        self.assertRaises(TypeError, failsafe_get(recipe, 'title'))
        res2 = failsafe_get(recipe, 'dish_title')
        self.assertEqual(u'potato salad', res2)
        res3 = failsafe_get(recipe, 'dish.title')
        self.assertEqual(u'potato salad', res3)
        ingredient1 = recipe.ingredients[0]
        res4 = failsafe_get(ingredient1, 'unit.abbr')
        self.assertEqual(u'pcs.', res4)
        APUs = failsafe_get(ingredient1, 'product.APUs')
        self.assertEqual(2, len(APUs))
        measured = failsafe_get(ingredient1, 'measured')
        self.assertEqual(3, measured)

    def test_update_status(self):
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        POST = MultiDict((('new_status', '0'),))
        request = DummyRequest(POST=POST,
                               user=User.fetch(email='user1@acme.com'))
        request.matchdict['id'] = recipe.id
        update_status_view(request)
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        self.assertEqual(0, recipe.status_id)

    def test_vote(self):
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        self.assertEqual(0, recipe.rating)
        post = MultiDict((
            ('recipe_id', recipe.id),
            ('vote_value', '-1')))
        request = DummyRequest(POST=post,
            user=User.fetch(email='user1@acme.com'))
        vote_view(request)
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        self.assertEqual(-1, recipe.rating)

    def test_add_comment_view(self):
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        author = User.fetch(email='user2@acme.com')
        post = MultiDict((
            ('recipe_id', recipe.id),
            ('text', u'Какой интересный рецепт!')))
        request = DummyRequest(POST=post, user=author)
        add_comment_view(request)
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        self.assertEqual(1, len(recipe.comments))
        comment = recipe.comments[0]
        self.assertEqual(u'Какой интересный рецепт!', comment.text)
        self.assertIs(author, comment.author)

class TestUserViews(unittest.TestCase):

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
            populate_test_data()

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
        register_view(request)
        user = User.fetch(email='test@acme.com')
        assert user is not None
        assert user.check_password(u'8Z然y落Σ#2就O')
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
        register_view(request)
        user = User.fetch(email='invalid@acme.com')
        assert user is None

    def test_register_existent_user(self):
        POST = MultiDict((
            ('email', 'user1@acme.com'),
            ('password', u'8765432'),
            ))
        request = DummyRequest(POST=POST)
        request.matchdict['next_path'] = '/dashboard'
        register_view(request)
        user = User.fetch(email='user1@acme.com')
        assert user.check_password(u'题GZG例没%07Z')

    def test_update_profile(self):
        POST = MultiDict((
            ('nickname', 'AcmeBOSS'),
            ('real_name', 'John Darko'),
            ('birthday', '1979-07-21'),
            ('location', 'Europe/London')
        ))
        request = DummyRequest(POST=POST,
                               user=User.fetch(email='user1@acme.com'))
        update_profile_view(request)
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

    def test_user_fav_dishes(self):
        potato_salad = Dish(u'potato salad')
        user=User.fetch(email='user1@acme.com')
        assert potato_salad in user.favourite_dishes

    def test_user_rep(self):
        user1=User.fetch(email='user1@acme.com')
        self.assertEqual(100, user1.profile.rep)
        user1.add_rep(20)
        user1.add_rep(-10)
        record = RepRecord.fetch(user_id=user1.id)
        self.assertEqual(-10, record.rep_value)
        self.assertEqual(110, user1.profile.rep)
        datetime_format = '%Y-%m-%d %H:%M'
        self.assertEqual(datetime.now().strftime(datetime_format),
            record.creation_time.strftime(datetime_format))
