from pecan                    import expose, request, response



class ErrorsController(object):


    @expose('json')
    def validation(self):
        response.status = 400
        return {'message':request.validation_errors}


    @expose('json')
    def database(self):
        response.status = 500
        return {'message':'Internal Server Error'}


    @expose('json')
    def notfound(self):
        response.status = 404
        return {'message':'Not Found'}


    @expose('json')
    def unable(self):
        """Unable to continue because of current state.
        Usually meant for payment instances that need to 
        be in a certain condition before modification occurs.
        """
        response.status = 400
        return {'message':'file uploaded is probably not tar.gz'}


    @expose('json')
    def not_implemented(self):
        """
        Unable to continue because the server could not fulfill 
        the request.
        Most of the time is due to a third party request like CIM.
        """
        response.status = 501
        return {'message':'server was not able to complete this request'}
