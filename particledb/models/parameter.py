from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from . import Base

class Parameter(Base):
    """ Represents a custom parameter for parts.
    """
    __tablename__ = 'parts_parameters'

    id = Column('id', Integer, primary_key=True)
    key = Column('key', String(255), nullable=False)
    value = Column('value', String(255), nullable=False)

    parts_id  = Column('parts_id', Integer, ForeignKey('parts.id'), nullable=False)
    part = relationship("Part", backref="parameters")
