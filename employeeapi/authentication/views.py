from django.shortcuts import render
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib import auth
import jwt
from django.core.cache import cache
from rest_framework import permissions

from .serializers import EmployeeSerializer, UpdateEmployeeSerializer, LoginSerializer
from .models import EmployeeModel
from .learn import BaseAPIView

# Create your views here.
class RegisterView(GenericAPIView):
    serializer_class = EmployeeSerializer

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        email = data.get("email", "")
        password = data.get("password", "")
        user = auth.authenticate(email=email, password=password)

        if user:
            auth_token = jwt.encode({"id": user.id}, settings.JWT_SECRET_KEY)
            serializer = EmployeeSerializer(user)
            data = {"access_token": auth_token}
            return Response(data, status=status.HTTP_200_OK)

        return Response(
            {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class UpdateEmployeeView(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UpdateEmployeeSerializer
    throttle_classes = (UserRateThrottle,)

    def retrieve(self, request, *args, **kwargs):
        # Caching employee details
        cache_key = f"user_details_{self.request.user.id}"
        data = cache.get(cache_key)
        if data:
            return Response(data)

        serializer = self.serializer_class(request.user)
        cache.set(cache_key, serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        employee_data = request.data
        serializer = self.serializer_class(
            request.user, data=employee_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeView(APIView):
    throttle_classes = (UserRateThrottle,)

    def get(self, request, id):
        try:
            user = EmployeeModel.objects.get(id=id)
            serializer = EmployeeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message": "No employee found for given employee id."},
                status=status.HTTP_404_NOT_FOUND,
            )


class DeleteEmployeeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, id):
        try:
            return EmployeeModel.objects.get(id=id)
        except EmployeeModel.DoesNotExist:
            raise Http404

    def delete(self, request, format=None):
        employee = self.get_object(self.request.user.id)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeList(ListAPIView):
    serializer_class = EmployeeSerializer
    # throttle_classes = (AnonRateThrottle,)

    def get_queryset(self):
        return list(EmployeeModel.objects.all())


class TestView(BaseAPIView):
    def get(self, request, partner_api_key):
        print(2)
        return super().get(request, partner_api_key)

    def execute_get(self, request):
        print(3)
        print(self.kp)
        return Response(status=status.HTTP_200_OK)