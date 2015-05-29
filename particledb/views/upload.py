from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import FileResponse

from ..models import DBSession, Manufacturer, UploadedFile
from ..utils.dbhelpers import get_by_or_404, get_or_404
from .base import BaseView

import os
import uuid
import shutil

class InvalidFileForUpload(Exception):
    pass

def store_file(request, post_file):
    # define some variables
    allowed_exts = request.registry.settings['upload_allowed_exts']
    allowed_exts = list(filter(lambda i: len(i) > 0, map(lambda i: i.lower(), allowed_exts.split("\n"))))
    upload_destination = request.registry.settings['upload_destination']
    filename = os.path.basename(post_file.filename)
    extension = os.path.splitext(filename)[1]
    file_path = os.path.join(upload_destination, '%s%s' % (uuid.uuid4(), extension))
    temp_file_path = file_path + '~'

    # check if uploaded file is valid
    if not extension[1:].lower() in allowed_exts:
        raise InvalidFileForUpload('Extension "%s" is not allowed' % extension)
    
    # write file to temporary location
    input_file = post_file.file
    input_file.seek(0)
    with open(temp_file_path, 'wb') as output_file:
        shutil.copyfileobj(input_file, output_file)

    # move temporary file to final destination
    os.rename(temp_file_path, file_path)

    # create database entry
    upload = UploadedFile.create_from(filename, file_path)
    DBSession.add(upload)
    return upload

def get_file_size(file):
    file.seek(0, 2) # Seek to the end of the file
    size = file.tell() # Get the position of EOF
    file.seek(0) # Reset the file position to the beginning
    return size
    
class UploadViews(BaseView):

    @view_config(
        route_name='upload_logo',
        renderer='json',
        request_method='POST'
    )
    def upload_logo(self):
        id = self.request.matchdict['manufacturer_id']
        manufacturer = get_or_404(Manufacturer, id)
        files, json_response = self.upload()
        if len(files) > 0:
            manufacturer.logo_image = files[0]
        return json_response
    
    def upload(self):
        json_data = []
        files = []
        
        for post_file in self.request.POST.getall('files[]'):
            try:
                file = store_file(self.request, post_file)
                files.append(file)
                json_data.append({
                    'name': file.filename,
                    'size': file.size,
                    'url': self.request.route_path('uploaded_file', uuid=file.uuid),
                })
            except InvalidFileForUpload as e:
                json_data.append({
                    'name': os.path.basename(post_file.filename),
                    'size': get_file_size(post_file.file),
                    'error': str(e),
                })

        return files, {'files': json_data}

    @view_config(
        route_name='uploaded_file',
        request_method='GET'
    )        
    def uploaded_file(self):
        file = get_by_or_404(UploadedFile, uuid=self.request.matchdict.get('uuid'))
        return FileResponse(
            file.get_full_path(self.request),
            request=self.request,
            content_type=file.content_type
        )
