import base64
from pecan                                     import response, abort, request
from pecan.secure                              import SecureController
from caral.controllers.simple                   import SimpleController
from caral.controllers.errors                   import ErrorsController
from caral.controllers.upload                   import UploadController


class RootController(object):


#    @classmethod
#    def check_permissions(cls):
#        # Make sure we have an Authorization header
#        # and that it's valid
#        try:
#            auth = request.headers.get('Authorization')
#            assert auth
#            decoded = base64.b64decode(auth.split(' ')[1])
#            username, password = decoded.split(':')
#
#            assert username == 'mirror'
#            assert password == 'caral'
#        except:
#            response.headers['WWW-Authenticate'] = 'Basic realm="Secure Area"'
#            abort(401)
#
#        return True    

    simple      = SimpleController()
    errors      = ErrorsController()
    upload      = UploadController()
