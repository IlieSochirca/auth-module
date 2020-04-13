"""
User Model
"""
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .config import _generate_jwt_token
from .managers import CustomUserManager


class Account(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model
    """
    username = None

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=100, default=None, null=True)
    last_name = models.CharField(max_length=100, default=None, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(_('staff status'), default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="created time")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated time")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    @property
    def token(self):
        return _generate_jwt_token(self.pk)

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
