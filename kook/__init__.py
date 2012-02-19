# -*- coding: utf-8 -*-

from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from sqlalchemy import engine_from_config

from .models import DBSession

def main(global_settings, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings)
    DBSession.configure(bind=engine)
    session_factory = UnencryptedCookieSessionFactoryConfig('5I73ZwNTzrF3gRoYmj')
    config = Configurator(settings=settings, session_factory=session_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('read_recipe', '/recipe/{title}')
    config.add_route('create_recipe', '/create_recipe')
    config.add_route('update_recipe', '/update_recipe/{title}')
    config.add_view('kook.views.recipe_index_view',
                    route_name='index',
                    renderer='kook:templates/index.mako')
    config.add_view('kook.views.read_recipe_view',
                    route_name='read_recipe',
                    renderer='kook:templates/read_recipe.mako')
    config.add_view('kook.views.create_recipe_view',
                    route_name='create_recipe',
                    renderer='kook:templates/create_recipe.mako')
    config.add_view('kook.views.update_recipe_view',
                    route_name='update_recipe',
                    renderer='kook:templates/update_recipe.mako')
    config.scan()
    return config.make_wsgi_app()