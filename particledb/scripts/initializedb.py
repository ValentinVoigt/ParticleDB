import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import DBSession, Base
from ..models import Manufacturer, Part, Package

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def create_models():
    m = Manufacturer(name='Maxim')
    yield m
    yield Part(mpn="TEST123", description="Simple Test component", manufacturer=m)
    
    for i in [2, 3]:
        yield Package(name="TO-220", pins=i)
        yield Package(name="TO-92", pins=i)
    
    for i in range(4, 28+1, 2):
        yield Package(name="DIP-%i" % i, pins=i)
    
def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        for model in create_models():
            DBSession.add(model)
