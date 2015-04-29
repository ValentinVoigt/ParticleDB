from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

from .package import Package
from .part import Part
from .manufacturer import Manufacturer

__all__ = ['Package', 'Part', 'Manufacturer']