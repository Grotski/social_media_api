from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager
)
from django.utils.translation import gettext as _


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]

    objects = UserManager()
