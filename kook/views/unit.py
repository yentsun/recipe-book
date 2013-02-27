# -*- coding: utf-8 -*-

from pyramid.httpexceptions import HTTPFound
from kook.models.recipe import Unit


def create(request):
    try:
        submit_path = request.current_route_url()
        next_url = request.route_path('products')
    except ValueError:
        submit_path = '/'
        next_url = '/'
    if request.POST:
        title = unicode(request.POST.getone('title'))
        new_unit = Unit(title)
        new_unit.save()
        request.session.flash(u'<div class="alert alert-success">'
                              u'Мера "%s" создана</div>'
                              % title)
        return HTTPFound(next_url)
    return {'unit': Unit.dummy(),
            'submit_path': submit_path,
            'units': Unit.fetch_all()}


def update(request):
    title = request.matchdict.get('title', None)
    unit = Unit.fetch(title)
    try:
        submit_path = request.current_route_url()
        next_url = request.route_path('products')
    except ValueError:
        submit_path = '/'
        next_url = '/'
    if request.POST:
        new_title = request.POST.getone('title')
        existing_unit = Unit.fetch(new_title)
        if existing_unit:
            existing_unit.abbr = request.POST.getone('abbr')
            for APU in unit.APUs:
                if APU.unit is unit:
                    APU.unit = existing_unit
        else:
            unit.title = new_title
            unit.abbr = request.POST.getone('abbr')
        request.session.flash(u'<div class="alert alert-success">'
                              u'Мера "%s" обновлена</div>' % unit.title)
        return HTTPFound(next_url)
    return {'unit': unit,
            'submit_path': submit_path,
            'units': Unit.fetch_all()}