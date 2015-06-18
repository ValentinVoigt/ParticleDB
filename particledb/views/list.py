from pyramid.view import view_config, view_defaults

from ..models import DBSession, Part, Package, Manufacturer

from .base import BaseView

from ..utils.pagination import Pagination

@view_defaults(request_method='GET')

class ListViewAbstract(BaseView):

    @property
    def nav_active(self):
        """ Currently active navigation entry has the same name as our route.
        """
        return self.request.matched_route.name

    def serve(self, query):
        pagination = Pagination(query, self.request)
        return {'pagination': pagination}

class ListView(ListViewAbstract):

    @view_config(
        route_name='list_parts',
        renderer='particledb:templates/list_parts.mak')
    def list_parts(self):
        return self.serve(DBSession.query(Part))

    @view_config(
        route_name='list_packages',
        renderer='particledb:templates/list_packages.mak')
    def list_packages(self):
        return self.serve(DBSession.query(Package))

    @view_config(
        route_name='list_manufacturers',
        renderer='particledb:templates/list_manufacturers.mak')
    def list_manufacturers(self):
        return self.serve(DBSession.query(Manufacturer))
