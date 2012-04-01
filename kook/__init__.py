# -*- coding: utf-8 -*-

from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.events import NewRequest
from .subscibers import handle_new_request
from sqlalchemy import engine_from_config
from pyramid_beaker import set_cache_regions_from_settings

from .models import DBSession

THEME = 'bootstrap'

def find_renderer(template_file, theme=THEME):
    return 'kook:templates/%s/%s' % (theme, template_file)

def main(global_settings, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings)
    DBSession.configure(bind=engine)
    set_cache_regions_from_settings(settings)
    session_factory = UnencryptedCookieSessionFactoryConfig('5I73ZwNTzrF3gRoYmj')
    config = Configurator(settings=settings, session_factory=session_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('dashboard', '/')
    config.add_route('read_recipe', '/recipe/{title}')
    config.add_route('create_recipe', '/create_recipe')
    config.add_route('update_recipe', '/update_recipe/{title}')
    config.add_route('delete_recipe', '/delete_recipe/{title}')
    config.add_view('kook.views.presentation.recipe_index_view',
                    route_name='dashboard',
                    renderer=find_renderer('read/dashboard.mako'))
    config.add_view('kook.views.presentation.read_recipe_view',
                    route_name='read_recipe',
                    renderer=find_renderer('read/read_recipe.mako'))
    config.add_view('kook.views.admin.create_recipe_view',
                    route_name='create_recipe',
                    renderer=find_renderer('create_update/create_recipe.mako'))
    config.add_view('kook.views.admin.update_recipe_view',
                    route_name='update_recipe',
                    renderer=find_renderer('create_update/update_recipe.mako'))
    config.add_view('kook.views.admin.delete_recipe_view',
                    route_name='delete_recipe')
    config.add_subscriber(handle_new_request, NewRequest)
    config.scan()
    return config.make_wsgi_app()