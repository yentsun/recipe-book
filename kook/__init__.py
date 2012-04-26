# -*- coding: utf-8 -*-

from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.events import NewRequest
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import authenticated_userid
from sqlalchemy import engine_from_config
from pyramid_beaker import set_cache_regions_from_settings
from subscibers import handle_new_request

from .models import DBSession, User

THEME = 'bootstrap'

def fetch_user(request):
    id = authenticated_userid(request)
    if id is not None:
        return User.fetch(id)

def find_renderer(template_file, theme=THEME):
    return 'kook:templates/%s/%s' % (theme, template_file)

def main(global_settings, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    authentication_policy = \
        AuthTktAuthenticationPolicy('0J/#.JD6;LGNR-',
                                    callback=User.group_finder)
    authorization_policy = ACLAuthorizationPolicy()
    engine = engine_from_config(settings)
    DBSession.configure(bind=engine)
    set_cache_regions_from_settings(settings)
    session_factory = UnencryptedCookieSessionFactoryConfig('5I73F3gRoYmj')
    config = Configurator(settings=settings, session_factory=session_factory,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy,
                          root_factory='kook.models.RootFactory')

    config.set_request_property(fetch_user, 'user', reify=True)

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('dashboard', '/')
    config.add_route('read_recipe', '/recipe/{title}/{author_id}')
    config.add_route('create_recipe', '/create_recipe')
    config.add_route('update_recipe', '/update_recipe/{title}')
    config.add_route('delete_recipe', '/delete_recipe/{title}')
    config.add_route('product_units', '/product_units/{product_title}')
    config.add_route('update_recipe_status',
                     '/update_recipe_status/{title}')

    config.add_route('register_user', '/register')
    config.add_route('login', '/login')
    config.add_route('update_profile', '/update_profile')
    config.add_route('logout', '/logout')

    config.add_view('kook.views.recipe.index_view',
                    route_name='dashboard',
                    renderer=find_renderer('read/dashboard.mako'))
    config.add_view('kook.views.recipe.read_view',
                    route_name='read_recipe',
                    renderer=find_renderer('read/read_recipe.mako'))
    config.add_view('kook.views.recipe.create_view',
                    route_name='create_recipe', permission='create',
                    renderer=find_renderer('create_update/create_recipe.mako'))
    config.add_view('kook.views.recipe.update_view',
                    route_name='update_recipe', permission='update',
                    renderer=find_renderer('create_update/update_recipe.mako'))
    config.add_view('kook.views.recipe.delete_view',
                    route_name='delete_recipe')
    config.add_view('kook.views.recipe.product_units_view',
                    route_name='product_units', renderer='json')
    config.add_view('kook.views.recipe.update_status_view',
                    route_name='update_recipe_status', renderer='json')
    config.add_view('kook.views.user.register_view',
                    route_name='register_user',
                    renderer=find_renderer('user/register.mako'))
    config.add_view('kook.views.user.login_view',
                    route_name='login',
                    renderer=find_renderer('user/login.mako'))
    config.add_view('kook.views.user.logout_view',
                    route_name='logout')
    config.add_view('kook.views.user.update_profile_view',
                    route_name='update_profile',
                    renderer=find_renderer('user/update_profile.mako'))
    config.add_subscriber(handle_new_request, NewRequest)
    config.scan()
    return config.make_wsgi_app()