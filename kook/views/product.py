# -*- coding: utf-8 -*-

from pyramid.httpexceptions import HTTPFound
from kook.models.recipe import Product, Unit, Ingredient


def index():
    return {'products': Product.fetch_all(order='title'),
            'units': Unit.fetch_all()}


def update(request):
    if 'title' in request.matchdict:
        title = unicode(request.matchdict['title'])
        product = Product.fetch(title) or Product(title)
    else:
        title = u''
        product = Product.dummy()
    try:
        update_path = request.current_route_url(title=title)
        next_url = request.route_path('products')
    except ValueError:
        update_path = '/'
        next_url = '/'
    if request.POST:
        new_title = unicode(request.POST.getone('title'))
        if new_title != product.title:
            existing_product = Product.fetch(new_title)
            if existing_product:
                for ingredient in Ingredient.fetch_all(product_title=title):
                    ingredient.product = existing_product
                product.delete()
                request.session.flash(u'<div class="alert alert-success">'
                                      u'Продукт "%s" заменен продуктом "%s"'
                                      u'</div>' % (title, new_title))
                return HTTPFound(next_url)
        product.update_from_multidict(request.POST)
        product.save()
        request.session.flash(u'<div class="alert alert-success">'
                              u'Продукт "%s" обновлен</div>' % product.title)
        return HTTPFound(next_url)
    return {'product': product, 'update_path': update_path,
            'units': Unit.fetch_all()}


def delete(request):
    """Fetch and delete a product"""
    title = unicode(request.matchdict['title'])
    victim = Product.fetch(title)
    victim.delete()