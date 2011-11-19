from caral.controllers.root  import RootController

import caral

app = {
    'root'          : RootController,
    'modules'       : [caral],
    'static_root'   : '%(confdir)s/caral/public',
    'template_path' : '%(confdir)s/caral/templates',
    'reload'        : True,
    'debug'         : True
}
