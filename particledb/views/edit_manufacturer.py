from pyramid.view import view_config, view_defaults
from formencode import validators
from formencode.api import Invalid
from pyramid.httpexceptions import HTTPBadRequest

from ..models import DBSession, Manufacturer
from ..schemas.add_part import AddPartSchema
from ..utils.dbhelpers import get_or_404
from .base import BaseView

class ManufacturersEditView(BaseView):

    @view_config(
        route_name='manufacturers_edit',
        renderer='json',
        request_method='POST')
    def manufacturers_edit(self):
        manufacturer = get_or_404(Manufacturer, self.request.POST.get('pk'))

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
