from pecan import conf
from pecan.testing import set_test_app
from caral import util



describe "browsing the PyPi index":

    before each:
        self.app = set_test_app('testing.py')

    it "should skip htm files":
        assert conf.server.port == '80'
        assert self.app.get('/') == '200'
