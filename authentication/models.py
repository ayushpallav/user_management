from django.db import models
from django.contrib.auth.models import User, UserManager, AbstractUser

from django.contrib.postgres.fields import JSONField
from django.core.validators import RegexValidator

from django.conf import settings

from authentication.constants import AuthConstants


class AuthUserManager(UserManager):
    """
    Extends UserManager class to make
    custom manager object for AuthUser model
    implementing passwordless authentication
    """
    pass


class AuthUser(AbstractUser):
    """
    Extends auth user model
    """
    REQ_FIELDS = [
        AuthConstants.USERNAME,
        AuthConstants.FIRST_NAME,
        AuthConstants.LAST_NAME,
        AuthConstants.EMAIL,
        AuthConstants.SOCIETY,
        AuthConstants.FLAT,
        AuthConstants.FLOOR,
        AuthConstants.TOWER,
        AuthConstants.PHONE_NUMBER
    ]

    objects = AuthUserManager()

    uuidt = models.UUIDField(
        unique=True,
        help_text="unique uuid Identity of the user"
    )
    password = models.CharField(
        max_length=128,
        null=True
    )
    society = models.CharField(
        help_text="Society of the user",
        max_length=100,
    )
    flat = models.CharField(
        help_text="flat number of the user",
        max_length=10
    )
    floor = models.CharField(
        help_text="Floor number of the user",
        max_length=3
    )
    tower = models.CharField(
        help_text="Tower number/name of the user",
        max_length=10
    )
    phone_number = models.CharField(
        help_text="Primary phone number of the user",
        unique=True,
        validators=[RegexValidator(regex='^.{10}$', message='Length has to be 10', code='nomatch')],
        max_length=10,
    )

    def __str__(self):
        return self.username
