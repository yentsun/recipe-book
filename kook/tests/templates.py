# -*- coding: utf-8 -*-

import unittest

from sqlalchemy.engine import engine_from_config
from webtest import TestApp
from paste.deploy.loadwsgi import appconfig
from pyramid import testing
from pyramid.testing import tearDown

from kook import main
from kook.models import DBSession
from kook.models.recipe import Recipe
from kook.scripts import populate_dummy_data


def post_login_request(suite):
    return suite.testapp.post('/login', ('email=user1@acme.com&'
                                         'password=%E9%A2%98GZG%E4%BE'
                                         '%8B%E6%B2%A1%2507Z'))


class FunctionalTests(unittest.TestCase):

    def setUp(self):
        settings = appconfig('config:testing.ini',
                             'main',
                             relative_to='../..')
        app = main({}, **settings)
        self.testapp = TestApp(app)
        self.config = testing.setUp()
        engine = engine_from_config(settings)
        DBSession.configure(bind=engine)
        populate_dummy_data(engine)

    def tearDown(self):
        DBSession.remove()
        tearDown()

    def test_index(self):
        self.testapp.get('/', status=200)

    def test_login_form(self):
        response = self.testapp.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('email' in response)
        self.assertTrue('password' in response)

    def test_login_success(self):
        response = post_login_request(self)
        self.assertEqual(response.status_code, 302)
        final_response = response.follow()
        self.assertTrue('alert-success' in final_response)
        self.assertTrue('user1@acme.com' in final_response)

    def test_login_fail(self):
        response = self.testapp.post('/login', ('email=user1@acme.com&'
                                                'password=wrong_password'))
        self.assertEqual(response.status_code, 200)
        self.failUnless('alert-error' in response)

    def test_logout(self):
        post_login_request(self)
        response = self.testapp.get('/logout')
        self.assertEqual(response.status_code, 302)
        final_response = response.follow()
        self.assertTrue('email' in final_response)
        self.assertTrue('password' in final_response)

    def test_dashboard(self):
        response = post_login_request(self)
        self.assertEqual(response.status_code, 302)
        final_response = response.follow()
        self.assertTrue('potato salad' in final_response)
        self.assertTrue('/update_recipe' in final_response)
        self.assertTrue('#upload_json' in final_response)

    def test_recipe_update_success(self):
        post_login_request(self)
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        response = self.testapp.get('/update_recipe/{id}'.format(id=recipe.ID))
        self.assertTrue('<small>potato salad</small>'
                        in response)
        form = response.form
        self.assertEqual('/update_recipe/{id}'.format(id=recipe.ID),
                         form.action)
        self.assertEqual('the fastest way', form['description'].value)
        self.assertEqual('Place potatoes in a large saucepan or Dutch oven '
                         'and cover with lightly salted water. Bring to a '
                         'boil and cook until tender',
                         form.fields['step_text'][0].value)
        # update success
        form['description'] = 'a fast way'
        form.set('product_title', 'lemon crush', index=2)
        form.set('measured_amount', '30', index=2)
        updated_response = form.submit()
        self.assertEqual(updated_response.status_code, 302)
        updated_response = updated_response.follow()
        updated_form = updated_response.form
        self.assertEqual('a fast way', updated_form['description'].value)
        self.assertEqual('lemon crush',
                         updated_form.fields['product_title'][2].value)
        self.assertEqual('30',
                         updated_form.fields['measured_amount'][2].value)

    def test_recipe_update_fail(self):
        post_login_request(self)
        recipe = Recipe.fetch_all(dish_title=u'potato salad')[0]
        response = self.testapp.get('/update_recipe/{id}'.format(id=recipe.ID))
        form = response.form
        form.set('product_title', ' ', index=2)
        updated_response = form.submit()
        self.assertEqual(updated_response.status_code, 200)
        self.assertTrue('error_data' in updated_response)

    def test_create_recipe_success(self):
        post_login_request(self)
        response = self.testapp.get('/update_recipe')
        form = response.form
        form['dish_title'] = u'Ачма'


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

    def test_dashboard_forbidden(self):
        self.testapp.get('/dashboard', status=403)