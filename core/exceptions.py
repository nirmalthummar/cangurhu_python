from django.utils.encoding import force_text
from rest_framework import exceptions
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


def core_exception_handler(exc, context):

    response = exception_handler(exc, context)
    handlers = {
        'ProfileDoesNotExist': _handle_generic_error,
        'ValidationError': _handle_generic_error
    }

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response):

    response.data = {
        'errors': response.data
    }

    return response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        data = response.data
        response.data = {}
        for field, value in data.items():
            if isinstance(value, list):
                value = value[0]
            if isinstance(value, dict):
                for k, v in value.items():
                    response.data[k] = v[0].title()
            response.data[field] = value

        # response.data = errors[0]
        # response.data['status'] = False
        # response.data['data'] = {}
        # response.data['code'] = response.status_code

    return response


class UnauthorizedError(exceptions.ValidationError):
    status_code = status.HTTP_401_UNAUTHORIZED


class UnauthorizedException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Mobile number is not verified'
    default_code = status.HTTP_403_FORBIDDEN

    def __init__(self, detail, field, status_code=440):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_text(detail)}
        self.detail = {'detail': force_text(self.default_detail)}


class CoreValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_text(detail)}
        self.detail = {'detail': force_text(self.default_detail)}
