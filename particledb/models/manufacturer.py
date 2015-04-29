from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from . import Base

class Manufacturer(Base):
    __tablename__ = 'manufacturers'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(45))
    logofile = Column('logofile', String(45))
    parts = relationship("Part", backref="manufacturer")
