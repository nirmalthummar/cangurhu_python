from rest_framework.exceptions import APIException
from rest_framework import status


def make_error_response_dict(message):
    return message


class ErrorResponseException(APIException):
    """
        Return http response in the format {"error: {
            "ref": 'SOME REFERENCE", "message": "SOME MESSAGE"}}
        """

    def __init__(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        self.detail = make_error_response_dict(f"{message}")
        self.status_code = status_code
