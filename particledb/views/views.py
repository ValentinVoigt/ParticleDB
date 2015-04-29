from pyramid.response import Response
from pyramid.view import view_config

from ..models import DBSession, Part

class BaseView:

    def __init__(self, request):
        self.request = request

    def navigation(self):
        """ Returns a list containing the left navigation panel's contents.
        The navigation entries consist of tuples in the following format:
        
        >>> (nav_active_key, title, href,)
        
        You can add None as separator between lists. You can also add plain
        strings instead of tuples or None to add non-clickable headlines.
        """
        return [
            ('listall', 'List of parts', self.request.route_path('listall'),),
            None,
            "Example",
            ('example', 'Example page', self.request.route_path('example'),),
        ]
        
class ExampleView(BaseView):

    nav_active = "example"

    @view_config(route_name='example', renderer='particledb:templates/example.mak')
    def example(request):
        return {'one': None, 'project': 'ParticleDB'}
        
class ListAllPartsView(BaseView):

    nav_active = "listall"
        
    @view_config(route_name='listall', renderer='particledb:templates/list.mak')
    def home(request):
        parts = DBSession.query(Part).all()
        return {'parts': parts}