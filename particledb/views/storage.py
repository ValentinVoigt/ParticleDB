from pyramid.view import view_config, view_defaults
from sqlalchemy.orm import subqueryload

from ..models import DBSession, Storage, StorageCell

from .base import BaseView

@view_defaults(request_method='GET')
class StorageView(BaseView):

    nav_active = 'storage'

    @view_config(
        route_name='storage',
        renderer='particledb:templates/storage.mak')
    def storage(self):
        storages = DBSession.query(Storage)
        storages = storages.options(subqueryload('cells').subqueryload('stocks'))
        storages = storages.all()
        return {'storages': storages}
