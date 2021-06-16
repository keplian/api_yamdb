from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    """Жанр."""
    name = models.CharField(
        'название жанра',
        max_length=200,
        help_text='Придумайте краткое и ёмкое название для жанра произведений')
    slug = models.SlugField(
        # unique=True,
        blank=True,
        null=True,
        max_length=100,
        verbose_name='url (slug)',
        help_text='Краткое, уникальное слово, которое будет '
                  'видно в ссылке на страницу жанра (часть URL)')

    class Meta:
        db_table = 'genres_title'
        verbose_name = 'genre'
        verbose_name_plural = 'Жанр'


class Category(models.Model):
    """Категория."""
    name = models.CharField(
        'название категории',
        max_length=200,
        help_text='Придумайте краткое и ёмкое название категории произведений')
    slug = models.SlugField(
        # unique=True,
        blank=True,
        null=True,
        max_length=100,
        verbose_name='url (slug)',
        help_text='Краткое, уникальное слово, которое будет '
                  'видно в ссылке на страницу категории (часть URL)')

    class Meta:
        db_table = 'categories_title'
        verbose_name = 'category'
        verbose_name_plural = 'Категория'


class Title(models.Model):
    """Произведения."""
    name = models.TextField()

    year = models.DateTimeField(
        'Год публикации', auto_now_add=True
    )

    description = models.TextField(
        'описание',
        blank=True,
        null=True,
        help_text='Опишите жанр так, чтобы пользователь мог легко  '
                  'определиться с выбором жанра для произведения.')

    genre = models.ForeignKey(
        'Genre',
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='жанр',
        help_text='Жанр произведения.',
        related_name='genre_titles')

    category = models.ForeignKey(
        'Category',
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='категория',
        help_text='Категория произведения.',
        related_name='category_titles')

    class Meta:
        db_table = 'titles_title'
        ordering = ('-year',)
        verbose_name = 'title'
        verbose_name_plural = 'произведения'


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    # title_id = models.ForeignKey(
    #     Title, on_delete=models.CASCADE, related_name='reviews'
    # )
    score = models.SmallIntegerField(10)
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    class Meta:
        db_table = 'reviews_review'
        ordering = ('-pub_date',)
        verbose_name = 'review'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author'],
                # fields=['title_id', 'author'],
                name='unique user_following',
            )
        ]


class Comment(models.Model):
    """Комментарий к отзыву."""
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произвидение',
        help_text='Произведение интелектуальное.',
        related_name='title')
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='отзыв',
        help_text='Отзыв на котоорый сделан комментарий.',
        related_name='review')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'comment'
        verbose_name_plural = 'комментарии'

