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
            ('home', 'Home', self.request.route_path('home'),),
            None,
            "Database contents",
            ('list_parts', 'List of parts', self.request.route_path('list_parts'),),
            ('list_packages', 'List of packages', self.request.route_path('list_packages'),),
            None,
            "Example",
            ('example', 'Example page', self.request.route_path('example'),),
        ]
