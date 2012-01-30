# -*- coding: utf-8 -*-

import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    metadata,
    Recipe,
    Product,
    Ingredient,
    Step,
    Action
    )

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
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    metadata.create_all(engine)
    with transaction.manager:
        recipe = Recipe(title=u'оливье',
                        description=u'Один из самых популярных салатов')
        potato = Product(title=u'картофель')
        carrot = Product(title=u'морковь')
        sausage = Product(title=u'колбаса вареная')
        onion = Product(title=u'лук репчатый')
        egg = Product(title=u'яйцо куриное')
        recipe.ingredients = [
            Ingredient(potato, amount=400),
            Ingredient(carrot, amount=150),
            Ingredient(sausage, amount=200),
            Ingredient(onion, amount=75),
            Ingredient(egg, amount=172)
        ]
        boil = Action(u'отварить')
        mix = Action(u'перемешать')
        recipe.steps = [
            Step(1, recipe.ingredients[0], boil, time_value=30),
            Step(1, recipe.ingredients[1], boil),
            Step(2, recipe.ingredients[0], Action(u'нарезать'), note=u'cut to little pieces'),
            Step(3, recipe.ingredients[0], mix),
            Step(3, recipe.ingredients[1], mix, time_value=10)
        ]
        recipe.save()
        recipe2 = recipe
        recipe2.title = u'Оливье 2'
        recipe2.save()