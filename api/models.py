from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=30, unique=True, validators=[username_validator]
    )
    email = models.EmailField(
        _("email address"),
    )
    role = models.CharField(max_length=30)
    description = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
