import unittest
from sqlalchemy.engine import engine_from_config
import transaction

from webtest import TestApp
from paste.deploy.loadwsgi import appconfig
from kook.models import DBSession
from kook.models.recipe import Recipe
from kook.models.sqla_metadata import metadata
from kook.tests.views import populate_test_data
from kook import main

class FunctionalTests(unittest.TestCase):

    def setUp(self):
        settings = appconfig('config:testing.ini',
                             'main',
                             relative_to='/home/yentsun/www/kook')
        app = main({}, **settings)
        self.testapp = TestApp(app)
        engine = engine_from_config(settings)
        DBSession.configure(bind=engine)
        metadata.create_all(engine)
        with transaction.manager:
            populate_test_data()

    def tearDown(self):
        transaction.abort()

    def test_read_recipe(self):
        recipe_to_test = Recipe.fetch_all(dish_title=u'potato salad')[0]
        res = self.testapp.get('/recipe/%s' % recipe_to_test.id, status=200)
        assert 'potato salad' in res.body
        assert 'The <strong>fastest</strong> way to cook potato salad'\
        in res.body