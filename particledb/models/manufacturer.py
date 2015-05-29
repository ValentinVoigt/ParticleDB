from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref, exc

from . import Base, DBSession

class Manufacturer(Base):
    """ Represents a part's manufacturer.
    """
    __tablename__ = 'manufacturers'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(45), unique=True, nullable=False)
    url = Column('url', String(255))
    parts = relationship("Part", backref="manufacturer")
    
    logo_image_id = Column(Integer, ForeignKey('uploaded_files.id'))
    logo_image = relationship("UploadedFile")

    @classmethod
    def by_name(cls, name):
        return DBSession.query(cls).filter(cls.name==name).one()

    @classmethod
    def get_or_create(cls, name):
        """ Fetches an Manufacturer instance by name.
        
        If there's no object named ``name``, a new one is created
        and added to the session.
        """
        try:
            return DBSession.query(cls).filter(cls.name==name).one()
        except exc.NoResultFound:
            ## exc.MultipleResultsFound impossible due to unique=True
            new = cls(name=name)
            DBSession.add(new)
            return new