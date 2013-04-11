import unittest
from sqlalchemy.engine import engine_from_config
from webtest import TestApp
from paste.deploy.loadwsgi import appconfig
from pyramid.testing import tearDown
from kook.models import DBSession
from kook.models.recipe import Recipe
from kook.models.sqla_metadata import metadata
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

    def test_read_recipe(self):
        recipe_to_test = Recipe.fetch_all(dish_title=u'potato salad')[0]
        res = self.testapp.get('/recipe/%s' % recipe_to_test.ID, status=200)
        assert 'potato salad' in res.body
        assert 'the fastest way' in res.body

    def test_index(self):
        self.testapp.get('/', status=200)