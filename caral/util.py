from threading          import Thread
from BeautifulSoup      import BeautifulSoup
import re
import os
import urlparse
import urllib
import urllib2
import Queue
import logging

from pecan import conf
logger = logging.getLogger(__name__)

pkg_queue = Queue.Queue()


try:
    from . import pkg_cache
    PKG_CACHE = pkg_cache.CACHE
except (ImportError, AttributeError):
    dump_cache(new=True)
    PKG_CACHE = {}


def dump_cache(new=False):
    if new:
        package_cache = {}
    else:
        package_cache = PKG_CACHE
    this_dir = os.path.abspath(os.path.dirname(__file__))
    cache_file = os.path.join(this_dir, 'pkg_cache.py')
    with open(cache_file, 'w') as dump:
        dump.write('CACHE = ' + repr(package_cache) + '\n')
    logger.debug('')
    logger.debug(repr(package_cache))
    logger.debug('cache has been dumped to: %s' % cache_file)


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
        for t in range(10):
            logger.debug("Spawned a synchronizer thread [%s]" % t)
            self.spawn_sync()

    def push_to_queue(self, metadata):
        """Submits a dictionary of stats to the queue"""
        logger.debug("pushing metadata to the queue")
        logger.debug("queue size is %s" % pkg_queue.qsize())
        pkg_queue.put(metadata)

    def spawn_sync(self):
        """Creates a thread that will fetch data from the queue"""
        sync = Synchronizer(pkg_queue)
        sync.setDaemon(True)
        sync.start()


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
        logger.debug('Attempting to verify url: %s' % url)
        if url.startswith('//'):
            url = 'http://' + url.lstrip('//')
        try:
            check_url = urllib.urlopen(url)
            return check_url.url
        except IOError, exc:
            logger.exception('Not able to verify url')
            return False

    def base_link(self):
        package_name = self.real_name(self.package_name)
        for mirror in conf.pypi_urls:
            try:
                failed = False
                address = self.real_url("%s%s" % (mirror, package_name))
                logger.debug('attempting to grab from address: %s' % address)
                html    = urllib2.urlopen(address).read()
                if self.not_modified(package_name, html, mirror):
                    logger.info('no new packages found, skipping: %s' % address)
                    continue
                soup    = BeautifulSoup(html)
                try:
                    divs =  soup.findAll('a')
                    return divs
                except IOError, e:
                    logger.exception(e)

            except:
                logger.exception('Could not get to mirror: %s' % mirror)
                failed = True
                continue
        if failed:
            raise PyPiNotFound
        return []

    # XXX Move this into its own thing
    def create_hash(self, name, html):
        import hashlib
        return hashlib.sha224(html).hexdigest()

    def not_modified(self, name, html, mirror):
        new_hash = self.create_hash(name, html)
        existing_hash = PKG_CACHE.get(mirror, {}).get(name)
        if new_hash == existing_hash:
            return True
        logger.info('package %s with hash %s has dated hash: %s' % (name, new_hash, existing_hash))
        PKG_CACHE.setdefault(mirror, {})[name] = new_hash
        dump_cache()
        return False

    def real_name(self, name):
        for mirror in conf.pypi_urls:
            try:
                failed = False
                address = self.real_url("%s" % mirror)
                logger.debug('attempting to find similar names on: %s' % address)
                html = urllib2.urlopen(address).read()
                soup = BeautifulSoup(html)
                try:
                    divs = soup.findAll('a')
                    for div in divs:
                        if div.text == name:
                            return name
                    for div in divs:
                        if div.text.lower() == name.lower():
                            return div.text
                except IOError, e:
                    logger.exception(e)

            except Exception:
                logger.exception('could not find name on: %s' % mirror)
                failed = True
                continue
        if failed:
            raise PyPiNotFound

    def should_skip_pkg(self, pkg):
        blacklist = ['.org', '.com', '.net', '.htm']
        logger.debug('pkg is ==> %s' % pkg)
        for b in blacklist:
            if pkg.endswith(b):
                return True
        if "://" in pkg:
            return True
        return False

    def url_end_part(self, url):
        if url.startswith('//'):
            logger.warning("swapping // for http:// in invalid url")
            url = 'http://' + url.lstrip('//')
        if url.endswith('/'): # handle trailing slashes
            url = url[:-1]
        return url.split('/')[-1].split('#')[0]

    def package_from_url(self, url):
        end_part = self.url_end_part(url)
        valid    = re.compile(r'[-a-z0-9._]+\.(tar|tar.gz|zip|tgz|bz2)$', re.IGNORECASE)
        if valid.match(end_part):
            return end_part
        logger.warning("url is not valid for fetching: %s" % url)
        logger.warning("end part was: %s" % end_part)
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


def real_name(name):
    """
    Attempt to match the real name of a package in a url. It is often the case
    that you might be dealing with a camel cased name but mirrors or installers
    will fix this problem for you by choosing the right one.
    """
    for mirror in conf.pypi_urls:
        try:
            address = mirror
            logger.debug('attempting to find similar names on: %s' % address)
            html = urllib2.urlopen(address).read()
            soup = BeautifulSoup(html)
            logger.debug('read pkg list from %s' % address)
            try:
                divs = soup.findAll('a')
                for div in divs:
                    if div.text == name:
                        logger.info('name of pkg exists: %s' % div.text)
                        return name
                for div in divs:
                    if div.text.lower() == name.lower():
                        logger.info('real name of pkg is: %s' % div.text)
                        return div.text
            except IOError:
                logger.exception('Unable to parse divs from %s' % address)

        except Exception:
            logger.exception('could not find name on: %s' % mirror)
            continue
    # if everything fails, just return what we got initially
    return name
