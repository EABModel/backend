from my_app import app
from flask import make_response
from functools import wraps
import json


class ClientError(Exception):
    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def _serialize(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = self.status_code
        return {'error': rv}

    def toJSON(self):
        return json.dumps(self._serialize())


class SchemaValidationError(Exception):
    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def _serialize(self):
        rv = {'message': self.message, 'status': self.status_code}
        return {'error': rv}

    def toJSON(self):
        return json.dumps(self._serialize())


def error_handling(common_error_msg="error"):
    def handle_errors(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except SchemaValidationError as error:
                return make_response(error.toJSON(), 400)
            except ClientError as error:
                return make_response(error.toJSON(), error.status_code)
            except Exception as error:
                app.logger.error(common_error_msg, error)
                raise error
        return decorated_function
    return handle_errors
