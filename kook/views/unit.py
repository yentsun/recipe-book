# -*- coding: utf-8 -*-

from pyramid.httpexceptions import HTTPFound
from kook.models.recipe import Unit

def update(request):
    title = request.matchdict.get('title', None)
    unit = Unit.fetch(title)
    try:
        submit_path = request.current_route_url()
        next = request.route_path('products')
    except ValueError:
        submit_path = '/'
        next = '/'
    if request.POST:
        new_title = request.POST.getone('title')
        existing_unit = Unit.fetch(new_title)
        if existing_unit:
            for product in unit.products:
                for APU in product.APUs:
                    if APU.unit is unit:
                        APU.unit = existing_unit
            unit.delete()
            request.session.flash(u'<div class="alert alert-success">'
                                  u'Мера "%s" заменена мерой "%s"</div>'
                                  % (title, new_title))
        else:
            unit.title = new_title
            unit.abbr = request.POST.getone('abbr')
            request.session.flash(u'<div class="alert alert-success">'
                                  u'Мера "%s" обновлена</div>' % unit.title)
        return HTTPFound(next)
    return {'unit': unit,
            'submit_path': submit_path,
            'units': Unit.fetch_all()}