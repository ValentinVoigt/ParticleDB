from math import ceil

from sqlalchemy import func

class Pagination(object):
    """ A dead-simple SQLAlchemy-based pagination helper-class.
    """

    def __init__(self, dataset, request, page_key='page', per_page=30, route_name=None):
        """ Initializes the pagination object.

        @param dataset SQLAlchemy query object
        @param request Pyramid's request object
        @param page_key Name of the page parameter in the matchdict-object
        @param per_page Number of items per page
        @param route_name Name of URL dispatch route to this pagination (defaults to current route!)
        """
        self.dataset = dataset
        self.request = request
        self.page_key = page_key
        self.per_page = per_page
        self.route_name = route_name if route_name else self.request.matched_route.name
        self.total = dataset.count()

    @property
    def page(self):
        """ Returns the current page number.
        """
        if self.page_key in self.request.matchdict:
            return int(self.request.matchdict[self.page_key])
        return 1

    @property
    def num_pages(self):
        """ Returns the number of pages available.
        """
        return int(ceil(self.total / float(self.per_page)))

    @property
    def has_prev(self):
        """ True if there's a previous page before the current page.
        """
        return self.page > 1

    @property
    def has_next(self):
        """ True if there's a next page after the current page.
        """
        return self.page < self.num_pages

    @property
    def current_dataset(self):
        """ Returns this page's objects as SQLAlchemy query.
        """
        return self.dataset.offset((self.page - 1) * self.per_page).limit(self.per_page)

    @property
    def is_empty(self):
        """ Returns true, if dataset is empty. False otherwise.
        """
        return self.total == 0

    @property
    def iterator(self):
        """ Iterate over this property to get all available page numbers as int.
        """
        for num in range(1, self.num_pages + 1):
            yield num

    def route_path(self, page):
        """ Internal helper-function.

        Returns the path a specific page. See __init__ for details.
        Returns "#" if page is invalid.
        """
        if page < 1 or page > self.num_pages:
            return "#"
        return self.request.route_path(self.route_name, **{self.page_key: page})
