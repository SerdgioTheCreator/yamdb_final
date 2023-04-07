"""Models module."""
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.validators import validate_year


class AbstractCategoryGenreModel(models.Model):
    """AbstractCategoryGenreModel method."""

    name = models.CharField(
        max_length=settings.NAME_LENGTH,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=settings.SLUG_LENGTH, unique=True,
        verbose_name='Slug', db_index=True
    )

    class Meta:
        """Meta class."""

        abstract = True
        ordering = ('-id', 'name',)

    def __str__(self):
        """Str method."""
        return self.name


class AbstractReviewCommentModel(models.Model):
    """AbstractReviewCommentModel method."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        """Meta class."""

        abstract = True
        ordering = ('-id', '-pub_date', )

    def __str__(self):
        """Str method."""
        return self.text[:settings.TEXT_CUTTER_30]


class Category(AbstractCategoryGenreModel):
    """Category method."""

    class Meta(AbstractCategoryGenreModel.Meta):
        """Meta class."""

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(AbstractCategoryGenreModel):
    """Genre method."""

    class Meta(AbstractCategoryGenreModel.Meta):
        """Meta class."""

        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Title method."""

    name = models.CharField(
        max_length=settings.TITLE_NAME_LENGTH,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        validators=(validate_year,),
        null=True,
        verbose_name='Год создания произведения',
        db_index=True
    )
    description = models.TextField(verbose_name='Описание произведения')
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        db_index=True,
        blank=True,
        verbose_name='Жанр',
        through='TitleGenre'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        """Meta class."""

        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-name',)

    def __str__(self):
        """Str method."""
        return self.name[:settings.TEXT_CUTTER_30]


class TitleGenre(models.Model):
    """TitleGenre method."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )

    class Meta:
        """Meta class."""

        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'


class Review(AbstractReviewCommentModel):
    """Review method."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    score = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Оценка',
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Оценка должна быть больше или равна 1.'
            ),
            MaxValueValidator(
                limit_value=10,
                message='Оценка должна быть меньше или равна 10.'
            )
        ],
        default=settings.DEFAULT_SCORE_VALUE
    )

    class Meta(AbstractReviewCommentModel.Meta):
        """Meta class."""

        default_related_name = 'reviews'
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review_per_author'
            )
        ]


class Comment(AbstractReviewCommentModel):
    """Comment method."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Комментарий'
    )

    class Meta(AbstractReviewCommentModel.Meta):
        """Meta class."""

        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
