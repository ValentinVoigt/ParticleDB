from pyramid.view import view_config, view_defaults

from ..models import DBSession, Part, Package

from .base import BaseView

@view_defaults(request_method='GET')
class ListView(BaseView):

    @property
    def nav_active(self):
        """ Currently active navigation entry has the same name as our route.
        """
        return self.request.matched_route.name

class ListPartsView(ListView):

    @view_config(
        route_name='list_parts',
        renderer='particledb:templates/list_parts.mak')
    def list_parts(request):
        parts = DBSession.query(Part).all()
        return {'parts': parts}
        
class ListPackagesView(ListView):

    @view_config(
        route_name='list_packages',
        renderer='particledb:templates/list_packages.mak')
    def list_packages(request):
        packages = DBSession.query(Package).all()
        return {'packages': packages}