from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    """Custom User model.

    User has roles:

    anonymous - can only read,
    user - can read and public reviews, rating; can raed and edit how own
           comments and rating
    moderator - like user, but also can delete or edit comments and reviews,
    admin -has all rules, can get rules to users
    """

    ROLE_CHOICES = [
        ("anon", "Anonymous"),
        ("user", "user"),
        ("moder", "moderator"),
        ("admin", "admin"),
    ]

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=30, unique=True, validators=[username_validator]
    )
    email = models.EmailField(
        _("email address"),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    description = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    def __str__(self):
        return f"{self.username}, has a {self.role} role"

    class Meta:
        verbose_name = "User"
