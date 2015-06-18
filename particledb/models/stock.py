from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from . import Base

class Stock(Base):
    """ Represents a number of parts with specific package in a storage cell.
    """
    __tablename__ = 'stocks'

    id = Column('id', Integer, primary_key=True)
    quantity = Column('quantity', Integer, nullable=True, default=1)

    part_id  = Column('parts_id', Integer, ForeignKey('parts.id'), nullable=False)
    cell_id  = Column('storages_cells_id', Integer, ForeignKey('storages_cells.id'), nullable=False)
    package_id  = Column('packages_id', Integer, ForeignKey('packages.id'))
