import os
from pecan import expose, request, redirect, conf


class UploadController(object):


    @expose('json')
    def index(self):
        if request.method == 'POST':
            upload   = request.POST.get('upload')
            filename = upload.filename
            file_obj = upload.file
            if not filename.endswith('tar.gz'):
                redirect('/errors/unable', internal=True)
            self.save_file(filename, file_obj)
            return dict()
        else:
            return "You probably want to POST a file right?"


    def save_file(self, filename, file_obj):
        dir_name = filename.split('.')[0].rstrip('0123456789-')
        dir_destination = "%s/%s" % (conf.app.static_root, dir_name)
        if not os.path.exists(dir_destination):
            os.mkdir(dir_destination)
        if filename in os.listdir(dir_destination):
            return # e.g. file is already there
        with open("%s/%s" % (dir_destination, filename), 'wb') as f:
            try:
                f.write(file_obj.getvalue())
            except AttributeError:
                f.write(file_obj.read())
