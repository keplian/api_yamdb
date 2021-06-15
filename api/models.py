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


class Titles(models.Model):
    name = models.TextField(
        "Название произведения",
        max_length=200,
        help_text="Введите название произведения",
    )
    year = models.DecimalField(
        "Год выпуска", max_digits=4, decimal_places=0, help_text="Год выпуска"
    )
    description = models.TextField(
        "Описание", help_text="Введите описание вашего произведения."
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория",
        related_name="Category",
    )
    genre = models.ForeignKey(
        "Genre",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Жанр",
        related_name="Genre",
    )

    def __str__(self) -> str:
        """Возвращает название произведения

        Ключевой аргумент:
        name -- Название произведения
        """
        return self.name

    class Meta:
        ordering = ("category",)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"


class Genre(models.Model):
    name = models.TextField(
        "Название жанра", max_length=200, help_text="Введите название жанра"
    )
    slug = models.SlugField("URL", unique=True)

    def __str__(self) -> str:
        """Возвращает название жанра

        Ключевой аргумент:
        name -- Название жанра
        """
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Category(models.Model):
    name = models.CharField(
        "Категория произведения",
        max_length=200,
        help_text="Введите категорию произведения.",
    )
    slug = models.SlugField("URL", unique=True)

    def __str__(self) -> str:
        """Возвращает тип произведения

        Ключевой аргумент:
        name -- Тип произведения
        """
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
