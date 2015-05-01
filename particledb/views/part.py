from pyramid.view import view_config, view_defaults
from ..models import DBSession, Part, Parameter
from .base import BaseView
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from sqlalchemy.orm.exc import NoResultFound

@view_defaults(request_method='GET')       
class PartView(BaseView):

    nav_active = 'list_parts'

    def navigation_hook(self):
        part = self.get_part()
        self.navigation_add_after(
            ('list_parts',),
            ('part', part.mpn, self.request.route_path('part', part_mpn=part.mpn), 'indent')
        )
    
    def get_part(self):
        try:
            mpn = self.request.matchdict['part_mpn']
            return DBSession.query(Part).filter(Part.mpn==mpn).one()
        except (IndexError, NoResultFound):
            raise HTTPNotFound("Part not found")

    @view_config(
        route_name='part',
        renderer='particledb:templates/part.mak')
    def part(self):
        return {'part': self.get_part()}

    @view_config(
        route_name='remove_part',
        request_method='POST')
    def remove_part(self):
        part = self.get_part()
        DBSession.delete(part)
        return HTTPFound(self.request.route_path("list_parts", page=1))

    @view_config(
        route_name='parameter_remove',
        request_method='POST',
        renderer='json')
    def parameter_remove(self):
        try:
            id = self.request.POST.get('id')
            parameter = DBSession.query(Parameter).filter(Parameter.id==id).one()
        except (IndexError, NoResultFound):
            raise HTTPNotFound("Parameter not found")

        DBSession.delete(parameter)
        return {}

    @view_config(
        route_name='parameter_edit',
        request_method='POST',
        renderer='json')
    def parameter_edit(self):
        try:
            id = self.request.POST.get('pk')
            parameter = DBSession.query(Parameter).filter(Parameter.id==id).one()
        except (IndexError, NoResultFound):
            raise HTTPNotFound("Parameter not found")

        col = self.request.POST.get('col')
        if not col in ['key', 'value']:
            raise HTTPBadRequest('Invalid column for data change')
        setattr(parameter, col, self.request.POST.get('value'))

        return {}