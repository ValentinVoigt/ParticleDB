from pyramid.view import view_config, view_defaults

from ..models import DBSession, Part

from .base import BaseView

@view_defaults(request_method='GET')
class SearchView(BaseView):

    @view_config(route_name='search_prefetch', renderer='json')
    def search_prefetch(self):
        return [{
            'mpn': part.mpn,
            'desc': part.description,
        } for part in DBSession.query(Part).all()]
