import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth.backends import ModelBackend

from .models import EmployeeModel


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None

        prefix, token = auth_data.decode("utf-8").split(" ")

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY)
            employee = EmployeeModel.objects.get(id=payload["id"])
            return (employee, token)

        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed("Your token is invalid")
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed("Your token is expired")
        except EmployeeModel.DoesNotExist as identifier:
            raise exceptions.AuthenticationFailed("Employee Not Found")

        return super().authenticate(request)


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            employee = EmployeeModel.objects.get(email=email, password=password)
            return employee
        except EmployeeModel.DoesNotExist:
            return None
