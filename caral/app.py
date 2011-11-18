from pecan       import make_app
from pecan.hooks import RequestViewerHook

def setup_app(config):

    app = make_app(
        config.app.root,
        static_root         = config.app.static_root,
        template_path       = config.app.template_path,
        debug               = config.app.debug,
        hooks               = [RequestViewerHook()]
    )

    return app
