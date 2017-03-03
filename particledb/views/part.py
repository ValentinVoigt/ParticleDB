from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest
from pyramid.decorator import reify
from sqlalchemy.orm.exc import NoResultFound

from ..models import DBSession, Part, Parameter
from .base import BaseView
from ..utils.dbhelpers import get_by_or_404, get_or_404

class PartView(BaseView):

    nav_active = 'list_parts'

    def navigation_hook(self):
        part = self.part
        self.navigation_add_after(
            ('list_parts',),
            ('part', part.mpn, self.request.route_path('part', part_mpn=part.mpn), 'indent')
        )

    @reify
    def part(self):
        return get_by_or_404(Part, mpn=self.request.matchdict.get('part_mpn'))

    @view_config(
        route_name='part',
        renderer='particledb:templates/part.mak')
    def show_part(self):
        return {'part': self.part}

    @view_config(
        route_name='remove_part',
        request_method='POST')
    def remove_part(self):
        DBSession.delete(self.part)
        return HTTPFound(self.request.route_path("list_parts", page=1))

    @view_config(
        route_name='parameter_remove',
        request_method='POST',
        renderer='json')
    def parameter_remove(self):
        id = self.request.POST.get('id')
        parameter = get_or_404(Parameter, id)
        DBSession.delete(parameter)
        return {}

    @view_config(
        route_name='parameter_edit',
        request_method='POST',
        renderer='json')
    def parameter_edit(self):
        id = self.request.POST.get('pk', '')
        parameter = get_or_404(Parameter, id)

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
        part = get_or_404(Part, self.request.POST.get('part'))
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
        part = get_or_404(Part, self.request.POST.get('part'))

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
