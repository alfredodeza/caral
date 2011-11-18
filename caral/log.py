from logging import getLogger

## Set logger objects for all modules
middleware  = getLogger('pypi.middleware')
util        = getLogger('pypi.util')
database    = getLogger('pypi.database')
server      = getLogger('pypi.web.server')
model       = getLogger('pypi.web.model')
