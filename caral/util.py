from threading          import Thread
from BeautifulSoup      import BeautifulSoup
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
            logger.info("grabbed all packages")
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
        self.save_to_dir = save_to_dir


    def real_url(self, url):
        check_url = urllib.urlopen(url)
        return check_url.url


    def base_link(self):
        try:
            address = self.real_url("http://pypi.python.org/simple/%s" % self.package_name)
            html = urllib2.urlopen(address).read()
            soup = BeautifulSoup(html)
        except:
            raise PyPiNotFound

        try:
            divs =  soup.findAll('a')
            return divs
        except IOError, e:
            logger.exception(e)


    def should_skip_href(self, href):
        whitelist = ['.tar.gz', '.zip', '.tgz']
        blacklist = ['tip.gz']
        for w in whitelist:
            if w in href:
                return False
        for b in blacklist:
            if b in href:
                return True
        return False


    def should_skip_pkg(self, pkg):
        blacklist = ['http', '.html', '.org', '.com', '.net', '.htm']
        for b in blacklist:
            if b in pkg:
                return True
        return False

    def clean_download_url(self, url):
        is_valid = not self.should_skip_href(url)
        if is_valid:
            return url.split('/')[-1].split('#')[0]
        return False

    def grab_all_packages(self):
        """
        Grabs all the packages for a given name
        """
        links = self.base_link()
        link_list = {}

        for link in links:
            href = link.get('href')
            pkg = self.clean_download_url(href)

            if not pkg:
                continue
            
            if link.get('rel') == "homepage":
                logger.debug('skipping link: %s' % link)
                continue
            if self.should_skip_href(href):
                logger.debug('skipping link, bad href: %s' % href)
                continue
            if self.should_skip_pkg(pkg):
                logger.debug('skipping link, bad pkg: %s' % pkg)
                continue

            if href.startswith('../../'):
                href = urlparse.urljoin(self.main_address, href.strip('../..'))

            pkg = self.clean_download_url(href)
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
                logger.debug("saving to directory: %s" % directory)
                urllib.urlretrieve(package_url, directory)
            except Exception, e:
                logger.exception("Skipping bad package (could not fetch url): %s" % version)


    def grab_package(self):
        """
        Grabs the latest and greates package
        """
        links = self.base_link()
        link_list = {}

        for link in links:
            href            = link.get('href')
            pkg             = link.text
            if link.get('rel') == "homepage" or 'tip.gz' in href or 'tar.gz' not in href:
                continue
            if 'index.html' in pkg or 'http' in pkg:
                continue
            if href.startswith('../../'):
                href = urlparse.urljoin(self.main_address, href.strip('../..'))

            link_list.update({pkg : href})

        # Some packages don't have source files in PyPi
        if not link_list:
            raise PyPiNotFound

        version = self.latest_version(link_list)

        if not os.path.exists(self.save_to_dir):
            os.mkdir(self.save_to_dir)
        package_url = self.real_url(link_list[version])
        urllib.urlretrieve(package_url, "%s/%s" % (self.save_to_dir, version))


    def latest_version(self, urls):
        keys = sorted(urls.keys(), reverse=True)
        return keys[0]

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
