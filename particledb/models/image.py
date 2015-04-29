from sqlalchemy import Column, Integer, String

from . import Base

class Image(Base):
    """ Represents an image.
    
    Images are stored in the filesystem and referenced from a table.
    """
    __tablename__ = 'images'

    id = Column('id', Integer, primary_key=True)
    path = Column('mpn', String(255), unique=True, nullable=False)
    alt = Column('alt', String(255))
