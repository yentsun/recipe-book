from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from sqlalchemy import engine_from_config

from .models import DBSession

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    session_factory = UnencryptedCookieSessionFactoryConfig('5I73ZwNTzrF3gRoYmj')
    config = Configurator(settings=settings, session_factory=session_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('recipe', '/recipe/{title}')
    config.add_route('add_recipe', '/add_recipe')
    config.add_view('kook.views.recipe_index_view',
        route_name='index', renderer='kook:templates/index.mako')
    config.add_view('kook.views.recipe_view',
        route_name='recipe', renderer='kook:templates/recipe.mako')
    config.add_view('kook.views.add_recipe_view',
        route_name='add_recipe', renderer='kook:templates/add_recipe.mako')
    config.scan()
    return config.make_wsgi_app()