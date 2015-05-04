from pyramid.view import view_config, view_defaults

from ..models import DBSession, Storage

from .base import BaseView

@view_defaults(request_method='GET')
class StorageView(BaseView):

    nav_active = 'storage'

    @view_config(
        route_name='storage',
        renderer='particledb:templates/storage.mak')
    def storage(self):
        storages = DBSession.query(Storage).all()
        return {'storages': storages}
