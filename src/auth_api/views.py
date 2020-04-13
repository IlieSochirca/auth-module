"""
Auth Views
"""
import smtplib

from django.contrib.auth import logout
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .config import get_logger
from .config import MailUtils
from .models import Account
from .serializers import LoginSerializer, AccountSerializer
from .config import generate_confirm_account_email_token, \
    confirm_token_for_account_confirmation

LOGGER = get_logger(__name__)


class RegisterView(generics.CreateAPIView):
    """
    Register View
    """
    permission_classes = (AllowAny,)
    serializer_class = AccountSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        LOGGER.info("Register new user: %s", serializer.data.get('email'))
        token = generate_confirm_account_email_token(serializer.data.get('email'))
        if user:
            try:
                MailUtils.send_user_awaiting_activation(user=user, token=token)
            except smtplib.SMTPException as err:
                LOGGER.error(err)
                return Response("Something went wrong once we tried to send you the email!", status=400)
            return Response(
                data={
                    "message": "An email confirmation was sent. \
                    Please click on the link in the email to confirm the account!",
                    "status": 201
                })


class ActivateView(APIView):
    """
    Activation View
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        email_token = self.request.GET.get("validationtoken")
        user_email = confirm_token_for_account_confirmation(email_token)
        if not user_email:
            return Response("The confirmation link is invalid or has expired.", status=404)
        user_to_activate = get_user_by_email(email=user_email, raise_exception=True)
        user_to_activate.is_active = True
        user_to_activate.save()
        return Response("Registration successfull!", status=200)


class LoginView(generics.CreateAPIView):
    """
    Login View
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        """
        Login CreateAPIView create method
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user_details = dict()
        user_details["first_name"] = user.first_name
        user_details["last_name"] = user.last_name
        LOGGER.info('User %s was logged in', user.email)
        return Response(serializer.data, headers={"Authorization": user.token}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    Logout View
    """

    def post(self, request):
        logout(request)
        return Response(status=204)


class MeView(APIView):
    """
    Get logged in user data
    """

    def get(self, request):
        serializer = AccountSerializer(request.user)
        return Response(serializer.data)


def get_user_by_email(email, raise_exception=False):
    user = Account.objects.filter(email=email).first()
    if user is None and raise_exception is True:
        raise Exception("User not found", status.HTTP_404_NOT_FOUND)
    return user
