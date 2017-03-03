from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from . import Base

association_table = Table('parts_has_files', Base.metadata,
    Column('parts_id', Integer, ForeignKey('parts.id')),
    Column('uploaded_files_id', Integer, ForeignKey('uploaded_files.id'))
)

class Part(Base):
    """ Represents a specific part.
    """
    __tablename__ = 'parts'

    id = Column('id', Integer, primary_key=True)
    mpn = Column('mpn', String(45), unique=True, nullable=False)
    description = Column('description', String(45))
    manufacturers_id  = Column('manufacturers_id', Integer, ForeignKey('manufacturers.id'))
    parameters = relationship("Parameter", order_by="Parameter.order", cascade="all, delete-orphan", single_parent=True)
    stocks = relationship("Stock", backref="part")
    files = relationship("UploadedFile", secondary=association_table, cascade="all, delete-orphan", single_parent=True)

    @property
    def in_stock(self):
        return len(self.stocks) > 0 and sum([i.quantity for i in self.stocks]) > 0
