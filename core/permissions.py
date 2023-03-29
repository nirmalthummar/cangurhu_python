import jwt

from django.conf import settings
from rest_framework import authentication, exceptions
from rest_framework import permissions
from django.contrib.auth import get_user_model
from core.token import token

User = get_user_model()


def decode_token(request):
    authentication_header_prefix = 'Bearer'
    auth_header = authentication.get_authorization_header(request).split()
    auth_header_prefix = authentication_header_prefix.lower()

    if not auth_header:
        return None

    if len(auth_header) == 1:
        return None

    elif len(auth_header) > 2:
        return None

    prefix = auth_header[0].decode('utf-8')
    token = auth_header[1].decode('utf-8')

    if prefix.lower() != auth_header_prefix:
        return None

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        msg = 'Signature has expired. Invalid token'
        raise exceptions.AuthenticationFailed(msg)
    except jwt.exceptions.DecodeError:
        msg = 'Invalid authentication. Could not decode token.'
        raise exceptions.AuthenticationFailed(msg)
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed()
    return payload


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return obj.pk == request.user.pk


class IsCook(permissions.BasePermission):
    def has_permission(self, request, view):
        auth_token = token.get_token(request)
        payload = token.get_payload(auth_token)
        role = payload.get('role')

        if role != User.COOK:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        auth_token = token.get_token(request)
        payload = token.get_payload(auth_token)
        role = payload.get('role')

        if role != User.COOK:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return obj.cook.pk == request.user.cook.pk


class IsCourier(permissions.BasePermission):
    def has_permission(self, request, view):
        auth_token = token.get_token(request)
        payload = token.get_payload(auth_token)
        role = payload.get('role')

        if role != User.COURIER:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        auth_token = token.get_token(request)
        payload = token.get_payload(auth_token)
        role = payload.get('role')

        if role != User.COURIER:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return obj.courier.pk == request.user.courier.pk


class IsCustomer(permissions.BasePermission):

    def has_permission(self, request, view):
        auth_token = token.get_token(request)
        payload = token.get_payload(auth_token)
        role = payload.get('role')

        if role != User.CUSTOMER:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        auth_token = token.get_token(request)
        payload = token.get_payload(auth_token)
        role = payload.get('role')

        if role != User.CUSTOMER:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False
        return True
        # return obj.customer.pk == request.user.customer.pk
