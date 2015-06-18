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
        self._navigation = [
            ('home', 'Home', self.request.route_path('home'),),
            None,
            "Database contents",
            ('list_parts', 'List of parts', self.request.route_path('list_parts', page=1),),
            ('list_packages', 'List of packages', self.request.route_path('list_packages', page=1),),
            ('list_manufacturers', 'List of manufacturers', self.request.route_path('list_manufacturers', page=1),),
            None,
            "Administrative",
            ('add_part', 'Add part', self.request.route_path('add_part'),),
            ('storage', 'Storage', self.request.route_path('storage'),),
        ]

        self.navigation_hook()
        return self._navigation

    def _find_nav_index(self, needle):
        """ Internal.

        Returns the index at which ``needle`` is found.
        Returns None if not found.
        """
        def matches(needle, nav):
            if type(needle) is str and type(nav) is str:
                return needle == nav
            elif type(needle) is tuple and type(nav) is tuple:
                return needle[0] == nav[0]
            return False

        idx = 0
        for nav in self._navigation:
            if matches(needle, nav):
                return idx
            idx += 1
        return None

    def navigation_hook(self):
        """ Implement this method in one of your subclasses to dynamically add
        entries to the navigation. Use
        """
        pass

    def navigation_add_after(self, after_what, what):
        """ Use this method in ``navigation_hook`` to dynamically add entries
        to the navigation structure.

        ``after_what`` describes the item, after which ``what`` is appended.

        Use a string for ``after_what`` for headlines or a tuple with one
        string item (nav_active_key) for ordinary navigation links.

        Example:
        >>> navigation_add_after("Headline", "Headline 2)
        Adds "Headline 2" after "Headline"

        >> navigation_add_after(("list_parts",), None)
        Adds a spacer after "list_parts" link.
        """
        self._navigation.insert(self._find_nav_index(after_what) + 1, what)

    def navigation_add_before(self, before_what, what):
        """ Use this method in ``navigation_hook`` to dynamically add entries
        to the navigation structure.

        ``before_what`` describes the item, before which ``what`` is inserted.

        See ``navigation_add_after`` for further details.
        """
        self._navigation.insert(self._find_nav_index(before_what), what)
