from sqlalchemy import Column, Integer, String

from . import Base

import os
import magic
import math

class UploadedFile(Base):
    """ Represents an uploaded file.

    Files are stored in the filesystem and referenced from a table.
    """
    __tablename__ = 'uploaded_files'

    id = Column('id', Integer, primary_key=True)

    # contains the original filename from the client
    filename = Column('name', String(255), nullable=False)

    # contains the actual filename from on the filesystem (UUID + ext)
    uuid = Column('uuid', String(255), unique=True, nullable=False)

    # contains the file size in bytes
    size = Column('size', Integer, nullable=True)

    # contains the mime type of the file (for HTTP header)
    content_type = Column('content_type', String(255))

    @classmethod
    def create_from(cls, original_name, file_path):
        """ Creates a new UploadedFile instance from the given parameters.
        Instance must be added to session manually.
        """
        return cls(
            uuid=os.path.basename(file_path),
            filename=original_name,
            size=os.path.getsize(file_path),
            content_type=str(magic.from_file(file_path, mime=True), encoding="ascii"),
        )

    def get_full_path(self, request):
        """ Returns the full path on local harddisk to the file.
        """
        uploads = request.registry.settings['upload_destination']
        full_path = os.path.join(uploads, self.uuid)
        return full_path

    def exists(self, request):
        """ Return true, if the file exists on harddisk and is readable.
        False otherwise
        """
        return os.path.isfile(self.get_full_path(request))

    def delete(self, request, ignore_missing=False):
        """ Deletes file on disk.
        Instance must be removed from session manually.
        """
        try:
            os.remove(self.get_full_path(request))
        except FileNotFoundError as e:
            if not ignore_missing:
                raise e

    @property
    def formatted_size(self):
        units = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
        unit = math.floor(math.log(self.size, 1024))
        unit = min([len(units) - 1, unit])
        return "%0.2f %s" % (self.size / math.pow(1024, unit), units[unit])
