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
from ..models import Manufacturer, Part, Package, Image

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def create_models():
    ## Maxim
    maxim_logo = Image(path='manufacturers/maxim.svg', alt="Maxim logo")
    yield maxim_logo
    maxim = Manufacturer(name='Maxim', logo_image=maxim_logo)
    yield maxim
    
    ## TI
    ti_logo = Image(path='manufacturers/ti.svg', alt="Texas Instruments logo")
    yield maxim_logo
    ti = Manufacturer(name='Texas Instruments', logo_image=ti_logo)
    yield ti

    ## Atmel
    atmel_logo = Image(path='manufacturers/atmel.svg', alt="Atmel logo")
    yield atmel_logo
    atmel = Manufacturer(name='Atmel', logo_image=atmel_logo)
    yield atmel

    ## Cypress
    cypress_logo = Image(path='manufacturers/cypress.svg', alt="Cypress logo")
    yield cypress_logo
    cypress = Manufacturer(name='Cypress', logo_image=cypress_logo)
    yield cypress
    
    ## Parts
    yield Part(mpn="TEST123", description="Simple test component", manufacturer=maxim)
    yield Part(mpn="TEST345", description="Another test component", manufacturer=ti)
    
    ## Packages
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
