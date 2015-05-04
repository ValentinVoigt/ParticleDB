from pyramid.view import view_config, view_defaults
from formencode.api import Invalid

from ..models import DBSession, Part, Manufacturer
from ..schemas.add_part import AddPartSchema
from .base import BaseView

class AddPartView(BaseView):

    nav_active = 'add_part'

    @view_config(
        route_name='add_part',
        renderer='particledb:templates/add_part.mak')
    def add_part(self):
        data = {
            'error': None,
            'success': None,
            'defaults': {'mpn': self.request.GET.get('mpn', '')},
            'new_part': None,
        }
        
        if self.request.method == "POST":
            try:
                fields = AddPartSchema().to_python(self.request.POST)
                manufacturer = Manufacturer.get_or_create(fields.get('manufacturer'))
                data['new_part'] = Part(
                    mpn=fields.get('mpn'),
                    description=fields.get('description'),
                    manufacturer=manufacturer
                )
                DBSession.add(data['new_part'])
                data['success'] = True
            except Invalid as e:
                data['defaults'] = self.request.POST
                data['error'] = e

        return data

class MPNCheckJsonView(BaseView):

    @view_config(
        route_name='mpn_check',
        renderer='json',
        request_method='POST')
    def mpn_check(self):
        mpn = self.request.POST.get("mpn", "")
        if len(mpn) == 0:
            return {'available': 0}
        count = DBSession.query(Part.id).filter(Part.mpn==mpn).count()
        available = 1 if count == 0 else 0
        return {'available': available}

    @view_config(
        route_name='manufacturers_prefetch',
        renderer='json',
        request_method='GET')
    def manufacturers_prefetch(self):
        return [{
            'name': manufacturer.name,
        } for manufacturer in DBSession.query(Manufacturer).all()]

    @view_config(
        route_name='descriptions_prefetch',
        renderer='json',
        request_method='GET')
    def description_prefetch(self):
        return [{
            'description': part.description,
        } for part in DBSession.query(Part).all()]
        