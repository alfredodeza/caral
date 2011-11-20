from threading          import Thread
from BeautifulSoup      import BeautifulSoup
import re
import os
import urlparse
import urllib
import urllib2
import Queue
import logging

logger = logging.getLogger(__name__)

class Synchronizer(Thread):
    """Checks the queue every n minutes and pushes
    the data to the database if it finds an item"""

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        logger.debug("thread and queue initialized")

    def run(self):
        logger.debug("running thread and looking into the queue")
        while True:
            metadata  = self.queue.get()
            name      = metadata.get('name')
            directory = metadata.get('directory')

            self.grab(name, directory)
            self.queue.task_done()

    def grab(self, name, directory):
        try:
            browse = BrowsePyPi(name, directory)
            browse.grab_all_packages()
            logger.info("grabbed all packages for %s" % name)
        except Exception, error:
            logger.exception("thread unable to grab packages: %s" % error)



class RequestParser(object):
    """Receives a dictionary with the request and arranges
    the data to pass to the Queue instance"""


    def __init__(self, test=False):
        self.queue = Queue.Queue()
        if not test:
            self.spawn_sync()


    def push_to_queue(self, metadata):
        """Submits a dictionary of stats to the queue"""
        self.queue.put(metadata)
        logger.debug("pushing metadata to the queue")


    def spawn_sync(self):
        """Creates a thread that will fetch data from the queue"""
        sync = Synchronizer(self.queue)
        sync.setDaemon(True)
        sync.start()
        logger.debug("spawned a thread")




class PyPiNotFound(Exception):
    def __init__(self):
        message = "Package not found"
        Exception.__init__(self, message)



class BrowsePyPi(object):


    def __init__(self, package_name, save_to_dir):
        self.package_name = package_name
        self.main_address = "http://pypi.python.org/"
        self.save_to_dir  = save_to_dir


    def real_url(self, url):
        check_url = urllib.urlopen(url)
        return check_url.url


    def base_link(self):
        try:
            address = self.real_url("http://pypi.python.org/simple/%s" % self.package_name)
            html    = urllib2.urlopen(address).read()
            soup    = BeautifulSoup(html)
        except:
            raise PyPiNotFound

        try:
            divs =  soup.findAll('a')
            return divs
        except IOError, e:
            logger.exception(e)


    def should_skip_pkg(self, pkg):
        blacklist = ['.org', '.com', '.net', '.htm']
        logger.debug('pkg is ==> %s' % pkg)
        for b in blacklist:
            if b in pkg:
                return True
        if "://" in pkg:
            return True
        return False


    def url_end_part(self, url):
        if url.endswith('/'): # handle trailing slashes
            url = url[:-1]
        return url.split('/')[-1].split('#')[0]


    def package_from_url(self, url):
        end_part = self.url_end_part(url)
        valid    = re.compile(r'[-a-z0-9.]+\.(tar|tar.gz|zip|tgz|bz2)$', re.IGNORECASE)
        if valid.match(end_part):
            return end_part
        logger.warning("url is not a valid for fetching: %s" % url)
        return False


    def grab_all_packages(self):
        """
        Grabs all the packages for a given name
        """
        links = self.base_link()
        link_list = {}

        for link in links:
            href = link.get('href')
            pkg  = self.package_from_url(href)

            if not pkg:
                continue
            if link.get('rel') == "homepage":
                logger.debug('skipping link: %s' % link)
                continue
            if self.should_skip_pkg(pkg):
                logger.debug('skipping link, bad pkg: %s' % pkg)
                continue
            if href.startswith('../../'):
                href = urlparse.urljoin(self.main_address, href.strip('../..'))

            link_list.update({pkg : href})

        # Some packages don't have source files in PyPi
        if not link_list:
            raise PyPiNotFound

        if not os.path.exists(self.save_to_dir):
            os.mkdir(self.save_to_dir)

        for version in link_list.keys():
            try:
                package_url = self.real_url(link_list[version])
                directory = "%s/%s" % (self.save_to_dir, version)
                if not self.file_already_exists(version, self.save_to_dir):
                    logger.debug("saving to directory: %s" % directory)
                    urllib.urlretrieve(package_url, directory)
            except Exception:
                logger.exception("Skipping bad package (could not fetch url): %s" % version)


    def latest_version(self, urls):
        keys = sorted(urls.keys(), reverse=True)
        return keys[0]


    def file_already_exists(self, filename, directory):
        if filename in os.listdir(directory):
            logger.debug("Skipping: %s already exists in: %s" % (filename, directory))
            return True
        return False


def set_logging(config=None):
    config = config or {
                        'log_enable'  : True,
                        'log_path'    : '/var/log/caral/caral.log',
                        'log_level'   : 'DEBUG',
                        'log_format'  : '%(asctime)s %(levelname)s %(name)s %(message)s',
                        'log_datefmt' : '%H:%M:%S' }
    enabled  = config['log_enable']
    log_path = config['log_path']

    if os.path.isdir(log_path):
        log_path = os.path.join(log_path, 'caral.log')

    levels = {
            'debug' : logging.DEBUG,
            'info'  : logging.INFO
    }

    level = levels.get(config['log_level'].lower())
    log_format = config['log_format']
    datefmt    = config['log_datefmt']

    logging.basicConfig(
            level    = level,
            format   = log_format,
            datefmt  = datefmt,
            filename = log_path,
            filemode = 'a'
    )


    if not enabled or log_path is None:
        logging.disable(logging.CRITICAL)
