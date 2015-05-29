from pyramid.view import view_defaults, view_config
from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import FileResponse

from ..models import DBSession, Manufacturer, Part, UploadedFile
from ..utils.dbhelpers import get_by_or_404, get_or_404
from .base import BaseView

import os
import uuid
import shutil

IMAGE_EXTENSIONS = [
    'png',
    'jpg',
    'jpeg',
    'gif',
    'svg',
]

class InvalidFileForUpload(Exception):
    pass

def store_file(request, post_file, allowed_extensions=None):
    # define some variables
    upload_destination = request.registry.settings['upload_destination']
    filename = os.path.basename(post_file.filename)
    extension = os.path.splitext(filename)[1]
    file_path = os.path.join(upload_destination, '%s%s' % (uuid.uuid4(), extension))
    temp_file_path = file_path + '~'

    # check if uploaded file is valid
    if allowed_extensions and not extension[1:].lower() in allowed_extensions:
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
    
@view_defaults(
    renderer='json',
    request_method='POST',
)
class UploadViews(BaseView):

    @view_config(route_name='upload_logo')
    def upload_logo(self):
        manufacturer = get_or_404(Manufacturer, self.request.matchdict['manufacturer_id'])
        files, json_response = self.upload(IMAGE_EXTENSIONS)
        if len(files) > 0:
            if manufacturer.logo_image is not None:
                manufacturer.logo_image.delete(self.request)
                DBSession.delete(manufacturer.logo_image)
            manufacturer.logo_image = files[0]
        return json_response
    
    @view_config(route_name='upload_file')
    def upload_file(self):
        part = get_or_404(Part, self.request.matchdict['part_id'])
        files, json_response = self.upload()
        part.files.extend(files)
        return json_response
    
    def upload(self, allowed_extensions=None):
        json_data = []
        files = []
        
        for post_file in self.request.POST.getall('files[]'):
            try:
                file = store_file(self.request, post_file, allowed_extensions)
                files.append(file)
                json_data.append({
                    'name': file.filename,
                    'size': file.size,
                    'formatted_size': file.formatted_size,
                    'url': self.request.route_path('uploaded_file', uuid=file.uuid),
                })
            except InvalidFileForUpload as e:
                json_data.append({
                    'name': os.path.basename(post_file.filename),
                    'size': get_file_size(post_file.file),
                    'error': str(e),
                })

        return files, {'files': json_data}

class UploadedFilesViews(BaseView):

    @view_config(
        route_name='delete_file',
        request_method='POST',
        renderer='json',
    )        
    def delete_file(self):
        file = get_or_404(UploadedFile, self.request.POST.get('id'))
        file.delete(self.request, ignore_missing=True)
        DBSession.delete(file)
        return {}

    @view_config(
        route_name='uploaded_file',
        request_method='GET',
    )        
    def uploaded_file(self):
        file = get_by_or_404(UploadedFile, uuid=self.request.matchdict.get('uuid'))
        return FileResponse(
            file.get_full_path(self.request),
            request=self.request,
            content_type=file.content_type
        )
