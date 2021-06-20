from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=30)
    bio = models.TextField(blank=True)
    confirmation_code = models.CharField(max_length=100, blank=True)


class Title(models.Model):
    """Название произведения."""

    name = models.TextField(
        "Название произведения",
        max_length=200,
        help_text="Введите название произведения",
    )
    year = models.DecimalField(
        'Год выпуска',
        max_digits=4,
        decimal_places=0,
        help_text='Год выпуска'
    )
    description = models.TextField(
        'Описание',
        help_text='Введите описание вашего произведения.'
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория",
        related_name="Category",
    )
    genre = models.ManyToManyField(
        "Genre",
        verbose_name="Жанр",
        related_name="Genre",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("year",)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"


class Category(models.Model):
    """Тип произведения."""

    name = models.CharField(
        "Категория произведения",
        max_length=200,
        unique=True,
        help_text='Введите категорию произведения.'
    )
    slug = models.SlugField(
        'URL',
        unique=True
    )
    slug = models.SlugField("URL", unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(models.Model):
    """Название жанра."""

    name = models.TextField(
        "Название жанра",
        max_length=200,
        unique=True,
        help_text="Введите название жанра"
    )
    slug = models.SlugField("URL", unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Review(models.Model):
    """Отзыв с оценкой (рейтингом)."""

    text = models.TextField()
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="Author"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="Title", blank=True
    )
    score = models.SmallIntegerField(10)
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        # db_table = "reviews_review"
        ordering = ("-pub_date",)
        verbose_name = "review"
        verbose_name_plural = "отзывы"


class Comment(models.Model):
    """Комментарий к отзыву."""

    text = models.TextField()
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="comments"
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="произвидение",
        help_text="Произведение интелектуальное.",
        related_name="title",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name="отзыв",
        help_text="Отзыв на котоорый сделан комментарий.",
        related_name="review",
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "comment"
        verbose_name_plural = "комментарии"
