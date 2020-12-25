from rest_framework import serializers
from django.contrib.auth.models import User

from .models import EmployeeModel


class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, min_length=8, write_only=True)
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)
    email = serializers.EmailField(max_length=255, min_length=4)
    age = serializers.IntegerField(min_value=12)
    designation = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = EmployeeModel
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "age",
            "designation",
        ]

    def validate(self, attrs):
        email = attrs.get("email", "")
        if EmployeeModel.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ("Email is already in use")})
        return super().validate(attrs)

    def create(self, validated_data):
        return EmployeeModel.objects.create(**validated_data)

    def update(self, instance, validated_data):

        password = validated_data.pop("password", None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class UpdateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeModel
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "age",
            "designation",
        ]

    def update(self, instance, validated_data):

        password = validated_data.pop("password", None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65, min_length=8, write_only=True)
    email = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = EmployeeModel
        fields = ["email", "password"]
