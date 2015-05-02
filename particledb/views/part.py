from pyramid.view import view_config, view_defaults
from ..models import DBSession, Part, Parameter
from .base import BaseView
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
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
        id = self.request.POST.get('pk', '')
        
        try:
            parameter = DBSession.query(Parameter).get(id)
        except (IndexError, NoResultFound):
            raise HTTPNotFound("Parameter not found")

        col = self.request.POST.get('name')
        if not col in ['key', 'value']:
            raise HTTPBadRequest('Invalid column for data change')
        setattr(parameter, col, self.request.POST.get('value'))

        return {}
        
    @view_config(
        route_name='parameter_add',
        request_method='POST',
        renderer='json')
    def parameter_add(self):
        try:
            id = self.request.POST.get('part')
            part = DBSession.query(Part).get(id)
        except (IndexError, NoResultFound):
            raise HTTPNotFound("Parameter not found")
        
        key = self.request.POST.get('key', '')
        value = self.request.POST.get('value', '')
        
        if len(key) == 0 or len(value) == 0:
            raise HTTPBadRequest('Parameters must no be empty')
        
        parameter = Parameter(key=key, value=value)
        part.parameters.append(parameter)
        
        # to obtain the new generated id
        DBSession.add(parameter)
        DBSession.flush()
        DBSession.refresh(parameter)
        
        return {'id': parameter.id}
        
        
    @view_config(
        route_name='parameter_reorder',
        request_method='POST',
        renderer='json')
    def parameter_reorder(self):
        try:
            id = self.request.POST.get('part')
            part = DBSession.query(Part).get(id)
        except (IndexError, NoResultFound):
            raise HTTPNotFound("Parameter not found")
        
        try:
            order = [int(i) for i in self.request.POST.get('order', '').split(',')]
        except ValueError:
            raise HTTPBadRequest('Given order list does contain non-numeric values')

        mymap = dict([(p.id, p) for p in part.parameters])
        
        if set(order) != set(mymap.keys()):
            raise HTTPBadRequest('Given order list does not match parameters')
        
        for i in range(0, len(part.parameters)):
            mymap[order[i]].order = i
        
        return {}
