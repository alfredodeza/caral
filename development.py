from caral.controllers.root  import RootController

import caral
#caral.util.set_logging()

app = {
    'root': 'caral.controllers.root.RootController',
    'modules': ['caral'],
    'static_root'   : '%(confdir)s/caral/public',
    'template_path' : '%(confdir)s/caral/templates',
    'reload'        : True,
    'debug'         : True
}

server = dict(
    port    = '9999',
    host    = '0.0.0.0'
)

engine      = 'sqlite:///caral.db'
ro_engine   = 'sqlite:///caral.db'

logging = {
    'loggers': {
        'root' : {'level': 'DEBUG', 'handlers': ['console']},
        'caral': {'level': 'DEBUG', 'handlers': ['console']}
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'formatters': {
        'simple': {
            'format': ('%(asctime)s %(levelname)-5.5s [%(name)s]'
                       '[%(threadName)s] %(message)s')
        }
    }
}

pypi_urls = ['http://cheese.yougov.net/simple/']
