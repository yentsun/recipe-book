# -*- coding: utf-8 -*-

import os
import sys
import transaction

from sqlalchemy import engine_from_config
from pyramid.paster import (get_appsettings, setup_logging)

from kook.models import DBSession
from kook.models.sqla_metadata import metadata
from kook.scripts import populate_dummy_data


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
        populate_dummy_data(engine)