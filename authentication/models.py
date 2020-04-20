from django.db import models
from django.contrib.auth.models import User

from django.contrib.postgres.fields import JSONField
from django.core.validators import RegexValidator

from django.conf import settings


class UserDetail(models.Model):
    """
    Extends user model of django.auth
    stores further information needed for a user
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    uuidt = models.UUIDField(
    	unique=True,
    	help_text="unique uuid Identity of the user"
	)
    address = models.CharField(
    	help_text="Address of the user",
        max_length=100,
    )
    phone_number = models.CharField(
    	help_text="Primary phone number of the user",
        validators=[RegexValidator(regex='^.{10}$', message='Length has to be 10', code='nomatch')],
        max_length=10,
    )

    def __str__(self):
        return self.user.username
