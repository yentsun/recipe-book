# -*- coding: utf-8 -*-

import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (get_appsettings, setup_logging)

from ..models import (DBSession, metadata, Recipe, Product, Ingredient, Step,
                      Unit, AmountPerUnit, User)

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings)
    DBSession.configure(bind=engine)
    metadata.create_all(engine)
    with transaction.manager:
        user1 = User.construct_from_dict({
            'email': 'user1@acme.com',
            'password': '123456'})
        print user1
        user1.save()
        recipe = Recipe(title=u'оливье',
            description=u'Один из самых популярных салатов',
            author=user1)
        potato = Product(title=u'картофель')
        sausage = Product(title=u'колбаса вареная')
        piece = Unit(u'штука', u'шт')
        bucket = Unit(u'ведро', u'вед')
        onion_piece = Unit(u'луковица')
        potato.APUs = [AmountPerUnit(100, piece),
                       AmountPerUnit(8000, bucket)]
        carrot = Product(title=u'морковь')
        onion = Product(title=u'лук репчатый')
        onion.APUs = [AmountPerUnit(75, onion_piece)]
        egg = Product(title=u'яйцо куриное')
        recipe.ingredients = [
            Ingredient(potato, amount=400, unit=piece),
            Ingredient(carrot, amount=150),
            Ingredient(sausage, amount=200),
            Ingredient(onion, amount=75),
            Ingredient(egg, amount=172)
        ]
        recipe.steps = [
            Step(1, u'все овощи отварить', time_value=30),
            Step(2, u'картофель и морковь очистить от кожицы', time_value=5),
            Step(3, u'овощи и колбасу нарезать и перемешать, заправляя майонезом', time_value=1),
            Step(4, u'салат украсить веткой петрушки', time_value=0)
        ]
        recipe.save()
        recipe2 = recipe
        recipe2.title = u'Оливье 2'
        recipe2.save()