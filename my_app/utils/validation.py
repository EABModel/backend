from my_app import app
from jsonschema import validate, ValidationError
from .errors import SchemaValidationError


def validate_request(request, schema):
    try:
        validate(request, schema)
    except ValidationError as error:
        app.logger.info("val error", error)
        raise SchemaValidationError(error.message, status_code=400)
    except Exception as error:
        app.logger.info("validation error", error)
        raise error
