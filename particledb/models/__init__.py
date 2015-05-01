from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

from .image import Image
from .manufacturer import Manufacturer
from .package import Package
from .parameter import Parameter
from .part import Part

__all__ = ['Base', 'DBSession', 'Image', 'Manufacturer', 'Package', 'Parameter', 'Part']