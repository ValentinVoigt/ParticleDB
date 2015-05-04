import formencode

from formencode import validators

from ..models import DBSession, Part

class UniqueMPN(formencode.FancyValidator):

    def _convert_to_python(self, value, state):
        query = DBSession.query(Part.id).filter(Part.mpn==value.strip())
        if query.count() > 0:
            raise formencode.Invalid('That MPN already exists', value, state)
        return value

class AddPartSchema(formencode.Schema):

    mpn = formencode.All(
        validators.String(not_empty=True, strip=True),
        UniqueMPN(),
    )
    description = validators.String()
    manufacturer = validators.String()
