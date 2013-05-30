import os
from urlparse import urljoin
import pecan
from pecan          import expose, conf, redirect
from caral.util      import BrowsePyPi, RequestParser, real_name
import logging

logger = logging.getLogger(__name__)
async_parser = RequestParser()

class DownloadController(object):


    def __init__(self, downloadName):
        self.name = downloadName
        self.dir  = "%s/%s" % (conf.app.static_root, self.name)
        self.not_found = False

    @expose('project.mak')
    def index(self):
        files = []
        try:
            self.files = files = os.listdir(self.dir)
        except:
            self.not_found = True

        # Always fire a thread to get packages
        logger.debug('spawning a thread to wget %s' % self.name)
        self.spawn_wget()

        # First point for redirection if we have never been requested the package before
        # XXX this logic is broken because the redirect should only happen if we are not 404'ing
        if self.not_found or not len(files):
            for mirror in pecan.conf.pypi_urls:
                address = "%s%s" % (mirror, self.name)
                logger.debug('redirecting to PyPi mirror [%s] since caral does not have package %s' % (mirror, self.name))
                pkg_name = real_name(self.name)
                redirect(urljoin(mirror, pkg_name))

        return dict(
            project_name = self.name,
            packages     = self.files)

    def spawn_wget(self):
        metadata = {'name': self.name, 'directory': self.dir}
        async_parser.push_to_queue(metadata)


    # XXX We don't use this anymore?
    def wget_package(self):
        try:
            browse = BrowsePyPi(self.name, self.dir)
            browse.grab_package()
        except:
            for mirror in pecan.conf.pypi_urls:
                try:
                    address = "%s%s" % (mirror, self.name)
                    logger.debug('redirecting to PyPi mirror [%s] since caral does not have package %s' % (mirror, self.name))
                    redirect(address)
                except:
                    continue


class SimpleController(object):

    @expose()
    def _lookup(self, downloadName, *remainder):
        return DownloadController(downloadName), remainder

    @expose('dirs.mak')
    def index(self):
        self.dir   = os.path.abspath(conf.app.static_root)
        self.files = os.listdir(self.dir)
        return dict(dir_names = self.files)
