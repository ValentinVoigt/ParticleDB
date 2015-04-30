from pyramid.view import view_config, view_defaults
from formencode import validators
from formencode.api import Invalid
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest

from ..models import DBSession, Manufacturer
from ..schemas.add_part import AddPartSchema
from .base import BaseView

class ManufacturersEditView(BaseView):

    @view_config(
        route_name='manufacturers_edit',
        renderer='json',
        request_method='POST')
    def manufacturers_edit(self):
        ## Get Manufacturer
        manufacturer_id = int(self.request.POST.get('pk', -1))
        manufacturer = DBSession.query(Manufacturer).get(manufacturer_id)
        if not manufacturer:
            raise HTTPNotFound('Manufacturer not found')
            
        ## Edit manufacturer
        if self.request.POST.get('name') == 'name':
            manufacturer.name = self.request.POST.get('value')
            return {'value': manufacturer.name}

        if self.request.POST.get('name') == 'url':
            raw_url = self.request.POST.get('value')    
            val = validators.URL(add_http=True)
            try:
                manufacturer.url = val.to_python(raw_url)
                return {'value': manufacturer.url}
            except Invalid as e:
                self.request.response.status = 400
                return {'message': str(e)}
