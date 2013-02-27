# -*- coding: utf-8 -*-

from pyramid.httpexceptions import HTTPFound
from kook.models.recipe import Product, Unit, AmountPerUnit


def create(request):
    try:
        submit_path = request.current_route_url()
        next_url = request.route_path('products')
    except ValueError:
        submit_path = '/'
        next_url = '/'
    if request.POST:
        amount = float(request.POST.getone('amount'))
        unit_title = request.POST.getone('unit_title')
        unit = Unit.fetch(unit_title) or Unit(unit_title)
        new_APU = AmountPerUnit(amount, unit)
        product_title = request.POST.getone('product_title')
        product = Product.fetch(product_title)
        product.APUs.append(new_APU)
        request.session.flash(u'<div class="alert alert-success">'
                              u'Мера "%s" для продукта "%s" создана</div>'
                              % (unit_title, product_title))
        return HTTPFound(next_url)
    return {'APU':AmountPerUnit.dummy(),
            'submit_path': submit_path,
            'products': Product.fetch_all(),
            'units': Unit.fetch_all()}


def update(request):
    unit_title = request.matchdict.get('unit_title', None)
    product_title = request.matchdict.get('product_title', None)
    APU = AmountPerUnit.fetch((product_title, unit_title))
    try:
        submit_path = request.current_route_url()
        next_url = request.route_path('products')
    except ValueError:
        submit_path = '/'
        next_url = '/'
    if request.POST:
        amount = float(request.POST.getone('amount'))
        APU.amount = amount
        request.session.flash(u'<div class="alert alert-success">'
                              u'Мера "%s" для продукта "%s" обновлена</div>'
                              % (unit_title, product_title))
        return HTTPFound(next_url)
    return {'APU': APU,
            'submit_path': submit_path,
            'products': Product.fetch_all(),
            'units': Unit.fetch_all()}