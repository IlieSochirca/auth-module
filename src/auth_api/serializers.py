"""
Auth Serializers
"""
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """
    first_name = serializers.CharField(required=False, validators=[UniqueValidator(queryset=Account.objects.all())])
    last_name = serializers.CharField(required=False, validators=[UniqueValidator(queryset=Account.objects.all())])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=Account.objects.all())])
    password = serializers.CharField(allow_blank=False, write_only=True)
    confirm_password = serializers.CharField(allow_blank=False, write_only=True)

    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data["password"]
        user = get_user_model().objects.create_user(email=validated_data["email"],
                                                    first_name=validated_data["first_name"],
                                                    last_name=validated_data["last_name"],
                                                    is_active=False)
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.pop("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match!")
        return data

    def update(self, *args, **kwargs):
        user = super().update(*args, **kwargs)
        p = user.password
        user.set_password(p)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    """
    Login Serializer
    """
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """
        Validates user data.
        """
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        else:
            data["user"] = user

        return data

    class Meta:
        model = Account
        fields = ("email", "password")


class PasswordResetSerializer(serializers.Serializer):
    """
    Password Reset Serializer
    """
    password = serializers.CharField(max_length=128)
    repeat_password = serializers.CharField(max_length=128)
