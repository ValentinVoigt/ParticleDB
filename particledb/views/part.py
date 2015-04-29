from pyramid.view import view_config, view_defaults

from ..models import DBSession, Part

from .base import BaseView

@view_defaults(request_method='GET')       
class PartView(BaseView):

    nav_active = None

    def get_part(self):
        mpn = self.request.matchdict['part_mpn']
        return DBSession.query(Part).filter(Part.mpn==mpn).one()

    @view_config(
        route_name='part',
        renderer='particledb:templates/part.mak')
    def part(self):
        return {'part': self.get_part()}
