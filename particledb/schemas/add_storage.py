import formencode

from formencode import validators

from ..models import DBSession, Storage

class UniqueName(formencode.FancyValidator):

    def _convert_to_python(self, value, state):
        query = DBSession.query(Storage.id).filter(Storage.name==value.strip())
        if query.count() > 0:
            raise formencode.Invalid('That name already exists', value, state)
        return value

class AddStorageSchema(formencode.Schema):

    name = formencode.All(
        validators.String(not_empty=True, strip=True),
        UniqueName(),
    )
    width = validators.Int(not_empty=True, min=1)
    height = validators.Int(not_empty=True, min=1)
