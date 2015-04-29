from pyramid.view import view_config

from .base import BaseView

class HomeView(BaseView):

    nav_active = "home"

    @view_config(route_name='home', renderer='particledb:templates/home.mak')
    def home(request):
        return {}
        
class ExampleView(BaseView):

    nav_active = "example"

    @view_config(route_name='example', renderer='particledb:templates/example.mak')
    def example(request):
        return {'one': None, 'project': 'ParticleDB'}
        
