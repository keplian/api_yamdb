from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=30)
    description = models.CharField(max_length=150, blank=True)
    confirmation_code = models.CharField(max_length=100, blank=True)
