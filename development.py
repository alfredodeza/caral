from caral.controllers.root  import RootController

import caral
caral.util.set_logging()

app = {
    'root'          : RootController,
    'modules'       : [caral],
    'static_root'   : '%(confdir)s/caral/public',
    'template_path' : '%(confdir)s/caral/templates',
    'reload'        : True,
    'debug'         : True
}

server = dict(
    port    = '80',
    host    = '0.0.0.0'
)

engine      = 'sqlite:///caral.db'
ro_engine   = 'sqlite:///caral.db'

