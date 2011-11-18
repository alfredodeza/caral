"""
caral: A test runner and DSL testing framework for writing readable, 
descriptive tests.

Version: 0.1.0

Usage:
    caral [options] 

"""

import json
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
        options = ['no-capture', '-s', 'fail', '-x', '-t', '-d', '--debug',
                   'dots', 'traceback', 'tracebacks', 'describe', 'it',
                   '--collect-match', '--collect-ci']
        coverage_options  = ['--show-missing', '--cover-dir', '--cover-report',
                            'cover']
        profiling_options = ['-p', 'profile']
        options.extend(coverage_options)
        options.extend(profiling_options)

        args = ArgOpts(options)
        args.parse_args(argv)
        
        if args.catches_help():
            self.msg(self.caral_help)

        if args.catches_version():
            message = "caral version %s" % __version__
            self.msg(message)

        if args.match:

            # Debugging option
            if args.has(['--debug']):
                self.config['debug'] = True
