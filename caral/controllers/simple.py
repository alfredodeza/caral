import os
from pecan          import expose, conf, redirect
from caral.util      import BrowsePyPi, RequestParser
import logging

logger = logging.getLogger(__name__)

class DownloadController(object):


    def __init__(self, downloadName):
        self.name = downloadName
        self.dir  = "%s/%s" % (conf.app.static_root, self.name)
        self.not_found = False


    @expose('project.mak')
    def index(self):
        try:
            self.files = os.listdir(self.dir)
        except:
            self.not_found = True
            logger.debug('redirecting to PyPi since caral does not have package %s' % self.name)
            redirect('http://pypi.python.org/simple/%s' % self.name)
        finally:
            if self.not_found:
                logger.debug('spawning a thread to wget %s' % self.name)
                self.spawn_wget()

        return dict(
            project_name = self.name,
            packages     = self.files
            )


    def spawn_wget(self):
        request = RequestParser()
        metadata = {'name': self.name, 'directory': self.dir}
        request.push_to_queue(metadata)


    def wget_package(self):
        try:
            browse = BrowsePyPi(self.name, self.dir)
            browse.grab_package()
        except:
            address = "http://pypi.python.org/simple/%s" % self.name
            logger.debug('redirecting to PyPi since caral does not have package %s' % self.name)
            redirect(address)


class SimpleController(object):
    

    @expose()
    def _lookup(self, downloadName, *remainder):
        return DownloadController(downloadName), remainder


    @expose('dirs.mak')
    def index(self):
        self.dir   = os.path.abspath(conf.app.static_root)
        self.files = os.listdir(self.dir)
        return dict(dir_names = self.files)
