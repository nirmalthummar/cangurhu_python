import jwt

from django.conf import settings
from rest_framework import authentication, exceptions


class Token:
    authentication_header_prefix = 'Bearer'

    def get_token(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        auth_token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None
        return auth_token

    def get_payload(self, auth_token):
        try:
            payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            msg = 'Signature has expired. Invalid token'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.exceptions.DecodeError:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()
        return payload


token = Token()
