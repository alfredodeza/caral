"""
caral: A test runner and DSL testing framework for writing readable, 
descriptive tests.

Version: 0.1.1

Usage:
    caral [options] 

"""

import sys
from caral.argopts    import ArgOpts

__version__ = '0.1.0'

class CaralCommands(object):


    def __init__(self, argv=None, parse=True, test=False):
        self.test  = test
        self.parse = parse
        
        if argv is None:
            argv = sys.argv
        if parse:
            self.parse_args(argv)


    def msg(self, msg, stdout=True):
        if stdout:
            sys.stdout.write(msg+'\n')
        else:
            sys.stderr.write(msg+'\n')
        if not self.test:
            sys.exit(1)


    def parse_args(self, argv):
        options = ['rm', 'upload', 'fetch']

        args = ArgOpts(options)
        args.parse_args(argv)
        
        if args.catches_help():
            self.msg(__doc__)

        if args.catches_version():
            message = "caral version %s" % __version__
            self.msg(message)

        if args.match:
            # don't do anything yet
            self.msg(__doc__)

        else:
            self.msg(__doc__)

