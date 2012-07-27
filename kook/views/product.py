# -*- coding: utf-8 -*-

from pyramid.httpexceptions import HTTPFound

from kook.models.recipe import Product, Unit

def index(request):
    return {'products': Product.fetch_all(order='title'),
            'units': Unit.fetch_all()}

def update(request):
    title = request.matchdict['title']
    try:
        update_path = request.current_route_url(title=title)
        next = request.route_path('products')
    except ValueError:
        update_path = '/'
        next = '/'
    product = Product.fetch(title)
    if request.POST:
        new_title = request.POST.getone('title')
        product.title = new_title
        product.save()
        request.session.flash(u'<div class="alert alert-success">'
                              u'Продукт "%s" обновлен</div>' % product.title)
        return HTTPFound(next)
    return {'product':product, 'update_path':update_path}

def delete(request):
    title = request.matchdict['title']
    victim = Product.fetch(title)
    victim.delete()
