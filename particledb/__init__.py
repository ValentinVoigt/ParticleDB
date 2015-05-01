from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import DBSession, Base

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    ## Routes
    config.add_route('home', '/')
    config.add_route('list_parts', '/list/parts/{page}')
    config.add_route('list_packages', '/list/packages/{page}')
    config.add_route('list_manufacturers', '/list/manufacturers/{page}')
    config.add_route('part', '/parts/{part_mpn}')
    config.add_route('add_part', '/add/part')
    config.add_route('remove_part', '/parts/{part_mpn}/remove')
    
    ## JSON API
    config.add_route('search_prefetch', '/json/search-prefetch')
    config.add_route('mpn_check', '/json/mpn-check')
    config.add_route('manufacturers_prefetch', '/json/manufacturers-prefetch')
    config.add_route('manufacturers_edit', '/json/manufacturers-edit')
    config.add_route('descriptions_prefetch', '/json/descriptions-prefetch')
    config.add_route('parameter_remove', '/json/parameter-remove')
    
    config.scan()
    return config.make_wsgi_app()
