# -*- coding: utf-8 -*-

import unittest
from sqlalchemy.engine import engine_from_config
from webtest import TestApp
from paste.deploy.loadwsgi import appconfig
from pyramid.testing import tearDown
from kook.models import DBSession
from kook.models.recipe import Recipe
from kook.tests.views import populate_test_data
from kook import main


class FunctionalTests(unittest.TestCase):

    def setUp(self):
        settings = appconfig('config:testing.ini',
                             'main',
                             relative_to='../..')
        app = main({}, **settings)
        self.testapp = TestApp(app)
        engine = engine_from_config(settings)
        DBSession.configure(bind=engine)
        populate_test_data(engine)

    def tearDown(self):
        DBSession.remove()
        tearDown()

    def test_index(self):
        self.testapp.get('/', status=200)

    def test_login_form(self):
        response = self.testapp.post('/login', ('email=user1@acme.com&'
                                                'password=%E9%A2%98GZG%E4%BE'
                                                '%8B%E6%B2%A1%2507Z'))
        self.assertEqual(response.status_code, 302)
        final_response = response.follow()
        self.failUnless('alert-success' in final_response)

    def test_read_recipe(self):
        recipe_to_test = Recipe.fetch_all(dish_title=u'potato salad')[0]
        res = self.testapp.get('/recipe/{id}'.format(id=recipe_to_test.ID),
                               status=200)
        assert 'potato salad' in res.body
        assert 'the fastest way' in res.body
        assert 'potato' in res.body
        assert 'lemon juice' in res.body
        assert 'Whisk lemon juice, oil, salt and pepper in a' in res.body

    def test_tag(self):
        tag_title = 'salad'
        res = self.testapp.get('/tag/{title}'.format(title=tag_title),
                               status=200)
        assert 'potato salad' in res.body

    def test_dish(self):
        dish_title = u'potato salad'
        recipe = Recipe.fetch_all(dish_title=dish_title)[0]
        res = self.testapp.get('/dish/{title}'.format(title=dish_title),
                               status=200)
        assert 'potato salad' in res.body
        assert 'the fastest way' in res.body
        assert '/recipe/{id}'.format(id=recipe.ID) in res.body