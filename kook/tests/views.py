# -*- coding: utf-8 -*-

import os
import json
import unittest
import transaction
import codecs

from datetime import date, datetime, time
from webob.multidict import MultiDict
from pyramid.testing import DummyRequest, setUp, tearDown
from pyramid.security import Deny
from pyramid.httpexceptions import HTTPError
from sqlalchemy import engine_from_config
from pyramid_beaker import set_cache_regions_from_settings
from paste.deploy.loadwsgi import appconfig
from kook.mako_filters import failsafe_get

from kook.models import (DBSession, UPVOTE, DOWNVOTE_REP_CHANGE,
                         UPVOTE_REP_CHANGE, DOWNVOTE_COST, DOWNVOTE)
from kook.models.recipe import (Recipe, Step, Product, Ingredient,
                                Unit, AmountPerUnit, Dish, Tag, DishImage)
from kook.models.user import User, Group, Profile, RepRecord
from kook.models.sqla_metadata import metadata
from kook.security import VOTE_ACTIONS
from kook.views.recipe import (create_update as create_update_recipe,
                               delete_view, index_view, read_view,
                               product_units_view, update_status_view,
                               vote_view, comment_view, delete_comment_view,
                               tag)
from kook.views.dish import (read as read_dish, update as update_dish)
from kook.views.product import (delete as delete_product,
                                update as update_product)
from kook.views.apu import create as create_APU, update as update_APU
from kook.views.unit import update as update_unit, create as create_unit
from kook.views.user import register_view, update_profile_view


def populate_test_data():

    #add users
    user1 = User.construct_from_dict({
        'email': 'user1@acme.com',
        'password': u'题GZG例没%07Z'})
    user1.groups = [Group('admins'), Group('upvoters'), Group('registered')]
    user1.favourite_dishes = [Dish(u'potato salad')]
    user1.profile = Profile(rep=120)
    user1.save()
    user2 = User.construct_from_dict({
        'email': 'user2@acme.com',
        'password': u'R52RO圣ṪF特J'})
    user2.groups = [Group('upvoters'), Group('registered')]
    user2.profile = Profile(nickname=u'Butters', real_name=u'Leopold Stotch',
                            rep=10)
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
        recipe = \
            Recipe.dummy(author=User.fetch(email=recipe_dict['author_email']))
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


class TestRecipeViews(unittest.TestCase):

    def setUp(self):
        settings = appconfig('config:testing.ini', 'main', relative_to='../..')
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
        all_dishes = Dish.fetch_all()
        self.assertEqual(3, len(all_dishes))
        self.assertEqual('simplyrecipes.com', potato_salad.image.credit)

    def test_recipe_index(self):
        all = Recipe.fetch_all()
        self.assertEqual(3, len(all))
        only_two = Recipe.fetch_all(limit=2)
        self.assertEqual(2, len(only_two))

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
        self.assertEqual(recipe.ingredients[0].get_measured(), '3')
        for ingredient in recipe.ingredients:
            if ingredient.product.title == u'лук':
                self.assertEqual(ingredient.get_measured(), 1)
        assert mix in recipe.steps
        datetime_format = '%Y-%m-%d %H:%M'
        self.assertEqual(datetime.now().strftime(datetime_format),
                         recipe.creation_time.strftime(datetime_format))
        self.assertEqual(time(minute=36), recipe.total_time)

    def test_ingredient_amounts(self):
        request = DummyRequest()
        recipe_to_test = Recipe.fetch_all(dish_title=u'spicy chick pea')[0]
        request.matchdict['id'] = recipe_to_test.id
        response = read_view(request)
        recipe = response['recipe']
        self.assertEqual(recipe.ingredients[2].amount, 5.5)
        self.assertEqual(recipe.ingredients[2].get_measured(), u'5½')
        self.assertEqual(recipe.ingredients[2].get_measured(False), u'5,5')
        self.assertEqual(recipe.ingredients[3].amount, 0.5)
        self.assertEqual(recipe.ingredients[3].get_measured(), u'½')

    def test_create_recipe(self):
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
            ('amount', '400,7'),
            ('unit_title', ''),
            ('product_title', u'сельдь'),
            ('amount', '200.5'),
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
        request.matchdict['fetch_image'] = False
        create_update_recipe(request)
        recipes = Recipe.fetch_all(dish_title=u'сельдь под шубой')
        assert len(recipes) is not 0
        self.assertEqual(recipes[0].dish.title, u'сельдь под шубой')
        self.assertEqual(len(recipes[0].ingredients), 5)
        potato = Product(u'картофель')
        potato_400g = Ingredient(potato, amount=400.7)
        assert potato in recipes[0].products
        assert potato_400g in recipes[0].ingredients
        assert Ingredient(Product(u'сельдь'), amount=200.5) in recipes[0].ingredients
        self.assertEqual(len(recipes[0].steps), 2)
        self.assertEqual(60, recipes[0].ordered_steps[1].time_value)

        #testing initial output
        request = DummyRequest(user=user)
        response = create_update_recipe(request)
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
        create_update_recipe(request)
        assert len(Recipe.fetch_all(dish_title=u'Уникальное блюдо')) is 0

    def test_update_recipe(self):
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
        request = DummyRequest(POST=POST,
                               user=User.fetch(email='user2@acme.com'))
        request.matchdict['fetch_image'] = False
        recipe_to_update = Recipe.fetch_all(dish_title=u'spicy chick pea')[0]
        request.matchdict['id'] = recipe_to_update.id
        create_update_recipe(request)
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
            '[{"amount": 8000.0, "abbr": "bkt.", "title": "bucket"}, '
            '{"amount": 100.0, "abbr": "pcs.", "title": "piece"}]', response)

        request.matchdict['product_title'] = u'batato'
        response = product_units_view(request)
        response = json.dumps(response)
        self.assertEqual('[]', response)

    def test_recipe_to_json(self):
        user = User.fetch(email='user1@acme.com')
        request = DummyRequest(user=user)
        recipe_to_test = Recipe.fetch_all(
            dish_title=u'potato salad',
            author_id=User.fetch(email='user1@acme.com').id)[0]
        request.matchdict['id'] = recipe_to_test.id
        response = read_view(request)
        recipe = response['recipe']
        recipe_json = json.dumps(recipe.to_dict())
        self.assertEqual(
            '{"ingredients": [{"amount": 300.0, "unit_title": "piece", '
            '"product_title": "potato"}, {"amount": 40.0, "unit_title": "", '
            '"product_title": "lemon juice"}, {"amount": 30.0, "unit_title": "", '
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
        recipe.attach_acl()
        assert (Deny, user.id, VOTE_ACTIONS) in recipe.__acl__

    def test_failsafe_get(self):
        none = None
        res0 = failsafe_get(none, 'dish_title')
        self.assertIs(None, res0)
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

    def test_update_status(self):
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        POST = MultiDict((('new_status', '0'),))
        request = DummyRequest(POST=POST,
                               user=User.fetch(email='user1@acme.com'))
        request.matchdict['id'] = recipe.id
        update_status_view(request)
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        self.assertEqual(0, recipe.status_id)

    def test_author_vote(self):
        user=User.fetch(email='user1@acme.com')
        self.config.testing_securitypolicy(userid=user.id, permissive=False)
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        self.assertEqual(0, recipe.rating)
        post = MultiDict((
            ('recipe_id', recipe.id),
            ('vote_value', '-1')))
        request = DummyRequest(POST=post, user=user)
        vote_view(request)
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        self.assertEqual(0, recipe.rating)

    def test_upvote(self):
        user=User.fetch(email='user2@acme.com')
        self.config.testing_securitypolicy(userid=user.id, permissive=True)
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        post = MultiDict((
            ('recipe_id', recipe.id),
            ('vote_value', '1')))
        request = DummyRequest(POST=post, user=user)
        vote_view(request)
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        self.assertEqual(1, recipe.rating)
        self.assertEqual(120+UPVOTE_REP_CHANGE, recipe.author.profile.rep)
        assert u'downvoters' in User.group_finder(user=recipe.author)
        self.assertIs(user.last_vote(recipe.id).value, UPVOTE)

    def test_downvote(self):
        user=User.fetch(email='user2@acme.com')
        self.config.testing_securitypolicy(userid=user.id, permissive=True)
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        post = MultiDict((
            ('recipe_id', recipe.id),
            ('vote_value', '-1')))
        request = DummyRequest(POST=post, user=user)
        vote_view(request)
        self.assertEqual(-1, recipe.rating)
        self.assertEqual(120+DOWNVOTE_REP_CHANGE, recipe.author.profile.rep)
        self.assertEqual(10+DOWNVOTE_COST, user.profile.rep)
        self.assertIs(user.last_vote(recipe.id).value, DOWNVOTE)

    def test_vote_sequence(self):
        user=User.fetch(email='user2@acme.com')
        self.config.testing_securitypolicy(userid=user.id, permissive=True)
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        post_upvote = MultiDict((
            ('recipe_id', recipe.id),
            ('vote_value', '1')))
        post_downvote = MultiDict((
            ('recipe_id', recipe.id),
            ('vote_value', '-1')))
        request_upvote = DummyRequest(POST=post_upvote, user=user)
        request_downvote = DummyRequest(POST=post_downvote, user=user)
        vote_view(request_upvote)
        vote_view(request_downvote)
        vote_view(request_upvote)
        vote_view(request_downvote)
        vote_view(request_upvote)
        self.assertEqual(1, recipe.rating)
        self.assertEqual(120+UPVOTE_REP_CHANGE+DOWNVOTE_REP_CHANGE,
                         recipe.author.profile.rep)
        self.assertIs(user.last_vote(recipe.id).value, UPVOTE)

    def test_comment_view(self):
        """

        """
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        author = User.fetch(email='user2@acme.com')
        post = MultiDict((
            ('recipe_id', recipe.id),
            ('comment_text', u'Какой интересный рецепт!')))
        request = DummyRequest(POST=post, user=author)
        comment_view(request)
        self.assertEqual(1, len(recipe.comments))
        comment = recipe.comments[0]
        self.assertEqual(u'Какой интересный рецепт!', comment.text)
        self.assertIs(author, comment.author)

        #test invalid comment
        post = MultiDict((
            ('recipe_id', recipe.id),
            ('comment_text', u'т прнес?')))
        request = DummyRequest(POST=post, user=author)
        self.assertRaises(HTTPError, comment_view, request)
        self.assertEqual(1, len(recipe.comments))

        #test update comment
        post = MultiDict((
            ('recipe_id', recipe.id),
            ('creation_time', comment.creation_time),
            ('comment_text', u'Какой неинтересный рецепт!')))
        request = DummyRequest(POST=post, user=author)
        comment_view(request)
        self.assertEqual(1, len(recipe.comments))
        comment = recipe.comments[0]
        self.assertEqual(u'Какой неинтересный рецепт!', comment.text)

    def test_comment_delete(self):
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        author = User.fetch(email='user2@acme.com')
        post = MultiDict((
            ('recipe_id', recipe.id),
            ('comment_text', u'Какой интересный рецепт!')))
        request = DummyRequest(POST=post, user=author)
        comment_view(request)
        assert len(recipe.comments) is 1
        comment = recipe.comments[0]
        request = DummyRequest(user=author)
        request.matchdict['recipe_id'] = recipe.id
        request.matchdict['creation_time'] = comment.creation_time
        delete_comment_view(request)
        transaction.commit()
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        self.assertEqual(0, len(recipe.comments))

    def test_dish_view(self):
        request = DummyRequest()
        request.matchdict['title'] = 'potato salad'
        response = read_dish(request)
        dish = response['dish']
        self.assertEqual(u'potato salad', dish.title)

    def test_update_dish_info(self):
        POST = MultiDict((
            ('title', u'potato salad'),
            ('description', u'A different description for potato salad'),
            ('tag', u'salad'),
            ('image_url', u'http://example.com/image.jpg'),
            ('image_credit', u''),
            ))
        request = DummyRequest(POST=POST)
        request.matchdict['title'] = 'potato salad'
        update_dish(request)
        potato_salad = Dish.fetch(u'potato salad')
        self.assertEqual([Tag(u'salad')], potato_salad.tags)
        self.assertEqual(u'http://example.com/image.jpg',
                         potato_salad.image.url)
        self.assertEqual('', potato_salad.image.credit)
        self.assertEqual(u'example.com', potato_salad.image.get_credit())

    # def test_update_dish_title(self):
    #     POST = MultiDict((
    #         ('title', u'batata salad'),
    #         ('description', u'A different description for potato salad'),
    #         ('tag', u'salad'),
    #         ('image_credit', ''),
    #         ('image_url', u'http://example.com/image.jpg'),
    #     ))
    #     request = DummyRequest(POST=POST)
    #     request.matchdict['title'] = u'potato salad'
    #     update_dish(request)
    #     batata_salad = Dish.fetch(u'batata salad')
    #     self.assertEqual([Tag(u'salad')], batata_salad.tags)
    #     assert Dish.fetch(u'potato salad') is None

    def test_tag_view(self):
        request = DummyRequest()
        request.matchdict['title'] = 'salad'
        response = tag(request)
        self.assertEqual(1, len(response['dishes']))
        self.assertEqual(u'potato salad', response['dishes'][0].title)

    def test_delete_product(self):
        request = DummyRequest()
        request.matchdict['title'] = u'potato'
        delete_product(request)
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        assert Product(u'potato') not in recipe.products
        self.assertEqual(2, len(recipe.ingredients))
        assert Product.fetch(u'potato') is None

    def test_update_product_new_value(self):
        POST = MultiDict((('title', 'botato'),))
        request = DummyRequest(POST=POST)
        request.matchdict['title'] = u'potato'
        update_product(request)
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        assert Product(u'potato') not in recipe.products
        assert Product(u'botato') in recipe.products

    def test_update_product_existing_value(self):
        POST = MultiDict((('title', 'batata'),))
        request = DummyRequest(POST=POST)
        request.matchdict['title'] = u'potato'
        update_product(request)
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        assert Product(u'potato') not in recipe.products
        assert Product(u'batata') in recipe.products
        assert Product.fetch(u'potato') is None

    def test_create_product_with_apu(self):
        POST = MultiDict((
            ('title', u'cucumber'),
            ('unit_title', u'piece'),
            ('amount', '100'),
            ('unit_title', u'bucket'),
            ('amount', '900'),
        ))
        request = DummyRequest(POST=POST)
        update_product(request)
#        cucumber = Product.fetch(u'cucumber')
#        assert cucumber
#        self.assertEqual(2, len(cucumber.APUs))
#        for apu in cucumber.APUs:
#            if apu.unit.title == u'piece':
#                self.assertEqual(100, apu.amount)

    def test_update_product_with_apu(self):
        POST = MultiDict((
            ('title', u'potato'),
            ('unit_title', u'piece'),
            ('amount', '100'),
            ('unit_title', u'bucket'),
            ('amount', '900'),
        ))
        request = DummyRequest(POST=POST)
        request.matchdict['title'] = u'potato'
        update_product(request)
        potato = Product.fetch(u'potato')
        assert potato
        self.assertEqual(2, len(potato.APUs))
        for apu in potato.APUs:
            if apu.unit.title == u'piece':
                self.assertEqual(100, apu.amount)
            if apu.unit.title == u'bucket':
                self.assertEqual(900, apu.amount)

    def test_create_APU(self):
        POST = MultiDict((
            ('unit_title', u'spoon'),
            ('product_title', u'lemon juice'),
            ('amount', u'30.5')
        ))
        request = DummyRequest(POST=POST)
        create_APU(request)
        lemon_juice = Product.fetch(u'lemon juice')
        assert AmountPerUnit(30.5, Unit(u'spoon')) in lemon_juice.APUs

    def test_update_APU(self):
        POST = MultiDict((
            ('unit_title', u'piece'),
            ('product_title', u'potato'),
            ('amount', u'90')
        ))
        request = DummyRequest(POST=POST)
        request.matchdict['unit_title'] = u'piece'
        request.matchdict['product_title'] = u'potato'
        update_APU(request)
        potato = Product.fetch(u'potato')
        assert AmountPerUnit(90, Unit(u'piece')) in potato.APUs
        assert AmountPerUnit(100, Unit(u'piece')) not in potato.APUs

    def test_create_unit(self):
        POST = MultiDict((
            ('title', u'spoon'),
            ('abbr', u'sp.'),
            ))
        request = DummyRequest(POST=POST)
        create_unit(request)
        assert Unit.fetch('spoon') is not None

    def test_update_unit(self):
        POST = MultiDict((
            ('title', u'piece_'),
            ('abbr', u'pc.'),
            ))
        request = DummyRequest(POST=POST)
        request.matchdict['title'] = u'piece'
        update_unit(request)
        potato = Product.fetch(u'potato')
        assert AmountPerUnit(100, Unit(u'piece_')) in potato.APUs
        assert AmountPerUnit(100, Unit(u'piece')) not in potato.APUs

    def test_update_unit_abbr(self):
        POST = MultiDict((
            ('title', u'piece'),
            ('abbr', u'pc.'),
            ))
        request = DummyRequest(POST=POST)
        request.matchdict['title'] = u'piece'
        update_unit(request)
        potato = Product.fetch(u'potato')
        self.assertEqual(u'pc.', potato.APUs[1].unit.abbr)


class TestUserViews(unittest.TestCase):

    def setUp(self):
        settings = appconfig('config:testing.ini', 'main', '../..')
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

#    def test_register_view(self):
#        POST = MultiDict((
#            ('email', 'test@acme.com'),
#            ('password', u'8Z然y落Σ#2就O'),
#            ))
#        request = DummyRequest(POST=POST)
#        request.matchdict['next_path'] = '/dashboard'
#        register_view(request)
#        user = User.fetch(email='test@acme.com')
#        assert user is not None
#        assert user.check_password(u'8Z然y落Σ#2就O')
#        self.assertEqual('registered', user.groups[0].title)
#        group_strings = User.group_finder(user=user)
#        assert 'registered' in group_strings
#        assert user.profile is not None
#        assert type(user.profile.registration_day) is date

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
        user = User.fetch(email='user1@acme.com')
        user2 = User.fetch(email='user2@acme.com')
        self.assertEqual(3, len(user.groups))
        self.assertEqual(2, len(user2.groups))
        group_strings = User.group_finder(user=user)
        assert u'admins' in group_strings
        assert u'upvoters' in User.group_finder(user=user2)
        assert u'registered' in User.group_finder(user=user2)

    def test_user_fav_dishes(self):
        potato_salad = Dish(u'potato salad')
        user=User.fetch(email='user1@acme.com')
        assert potato_salad in user.favourite_dishes

    def test_user_rep(self):
        user1=User.fetch(email='user1@acme.com')
        self.assertEqual(120, user1.profile.rep)
        user1.add_rep(20, 'test 1')
        user1.add_rep(-10, 'test 2')
        record = RepRecord.fetch(user_id=user1.id)
        self.assertEqual(-10, record.rep_value,)
        self.assertEqual(130, user1.profile.rep)
        datetime_format = '%Y-%m-%d %H:%M'
        self.assertEqual(datetime.now().strftime(datetime_format),
                         record.creation_time.strftime(datetime_format))

    def test_general(self):
        butters = User.fetch(email='user2@acme.com')
        self.assertEqual(butters.display_name, 'Butters')