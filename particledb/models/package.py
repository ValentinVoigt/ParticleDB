from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from . import Base

class Package(Base):
    """ Represents a part's package (like TO-220).
    """
    __tablename__ = 'packages'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(45), nullable=False)
    pins = Column('pins', Integer, nullable=False)
    picture = Column('description', String(45))
