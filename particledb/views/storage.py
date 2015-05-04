from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.orm import subqueryload
from formencode.api import Invalid

from ..models import DBSession, Storage, StorageCell
from ..schemas.add_storage import AddStorageSchema
from ..utils.dbhelpers import get_or_404
from .base import BaseView

@view_defaults(request_method='GET')
class StorageViews(BaseView):

    nav_active = 'storage'

    @view_config(
        route_name='storage',
        renderer='particledb:templates/storage.mak')
    def storage(self):
        storages = DBSession.query(Storage)
        storages = storages.options(subqueryload('cells').subqueryload('stocks'))
        storages = storages.all()
        return {'storages': storages}
        
@view_defaults(request_method='POST')
class StorageJsonViews(BaseView):

    @view_config(
        route_name='storage_add',
        renderer='json')
    def storage_add(self):
        try:
            fields = AddStorageSchema().to_python(self.request.POST)
            storage = Storage(
                name=fields.get('name'),
                width=fields.get('width'),
                height=fields.get('height')
            )
            DBSession.add(storage)
            return {'status': True}
        except Invalid as e:
            return {'status': False, 'message': str(e)}

    @view_config(
        route_name='storage_remove')
    def storage_remove(self):
        storage = get_or_404(Storage, self.request.POST.get('id'))
        DBSession.delete(storage)
        return HTTPFound(self.request.route_path("storage"))
