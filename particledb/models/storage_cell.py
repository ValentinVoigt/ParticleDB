from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from . import Base

class StorageCell(Base):
    """ Represents a storage container's single cell.
    """
    __tablename__ = 'storages_cells'

    id = Column('id', Integer, primary_key=True)
    number = Column('number', Integer, nullable=False)
    storage_id  = Column('storage_id', Integer, ForeignKey('storages.id'))
    stocks = relationship("Stock", backref="storage_cell")