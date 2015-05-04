from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from . import Base
from .storage_cell import StorageCell

class Storage(Base):
    """ Represents a storage container.
    """
    __tablename__ = 'storages'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(255), nullable=False, unique=True)
    width = Column('width', Integer, nullable=False)
    height = Column('height', Integer, nullable=False)
    cells = relationship("StorageCell", backref="storage", lazy='subquery')
    
    class Row():

        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

        def iter_cells(self):
            for col in range(0, self.storage.width):
                number = self.row * self.storage.width + col + 1
                yield self.storage._get_cell_by_number(number)
    
    def _get_cell_by_number(self, number):
        try:
            return list(filter(lambda x: x.number == number, self.cells))[0]
        except IndexError as e:
            cell = StorageCell(number=number)
            self.cells.append(cell)
            return cell
    
    def iter_rows(self):
        for row in range(0, self.height):
            yield Storage.Row(storage=self, row=row)
