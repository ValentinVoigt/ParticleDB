from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.inspection import inspect
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
DeclarativeBase = declarative_base()

class Base(DeclarativeBase):
    """ Base model for all models.
    """
    __abstract__ = True

    @classmethod
    def get(cls, *args):
        """ Returns object by primary ID.
        Returns None if object is not found.
        """
        primary_keys = [i.key for i in inspect(cls).primary_key]
        filter_ = dict(zip(primary_keys, args))
        return DBSession.query(cls).filter_by(**filter_).first()

    @classmethod
    def get_by(cls, **kwargs):
        """ Returns the first object by given filter.
        Returns None if object is not found.
        """
        return DBSession.query(cls).filter_by(**kwargs).first()

from .manufacturer import Manufacturer
from .package import Package
from .parameter import Parameter
from .part import Part
from .stock import Stock
from .storage import Storage
from .storage_cell import StorageCell
from .uploaded_file import UploadedFile

__all__ = [
    'Base', 'DBSession', 'Manufacturer', 'Package', 'Parameter',
    'Part', 'Stock', 'Storage', 'StorageCell', 'UploadedFile',
]
