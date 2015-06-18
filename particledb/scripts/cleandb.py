import os
import sys
import transaction

from pyramid.paster import bootstrap
from ..models import DBSession, UploadedFile

def usage():
    cmd = os.path.basename(sys.argv[0])
    print('usage: %s <config_uri> [--clean]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

def main():
    if not len(sys.argv) in (2, 3):
        usage()

    clean = False
    if len(sys.argv) == 3:
        if sys.argv[2] != '--clean':
            usage()
        clean = True

    config_uri = sys.argv[1]
    request = bootstrap(config_uri)['request']

    upload_destination = request.registry.settings['upload_destination']
    uuid_map = {}

    for file in DBSession.query(UploadedFile).all():
        if not file.exists(request):
            if clean:
                file.delete(request, ignore_missing=True)
                DBSession.delete(file)
                print("%s (%s) was missing; removed" % (file.filename, file.formatted_size))
            else:
                print("%s (%s) is missing" % (file.filename, file.formatted_size))
        else:
            uuid_map[file.uuid] = file

    for path in os.listdir(upload_destination):
        if len(path) < 36: # UUIDs have at least 36 letters
            continue
        if not path in uuid_map:
            if clean:
                os.remove(os.path.join(upload_destination, path))
                print("%s was not in database; removed" % path)
            else:
                print("%s is not in database" % path)

    if not clean:
        print("\nUse --clean to remove those files and database entries.")
    else:
        transaction.commit()
