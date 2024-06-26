"""Serializers module."""
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from api_yamdb.settings import (AUTH_CONF_CODE_MAXLENGTH, AUTH_EMAIL_MAXLENGTH,
                                AUTH_USERNAME_MAXLENGTH)

from .validators import validate_username, validate_year


class CategoriesSerializer(serializers.ModelSerializer):
    """CategoriesSerializer method."""

    class Meta:
        """Meta class."""

        fields = ('name', 'slug')
        model = Category
        extra_kwargs = {'slug': {'required': True}}


class GenreSerializer(serializers.ModelSerializer):
    """GenreSerializer method."""

    class Meta:
        """Meta class."""

        fields = ('name', 'slug')
        model = Genre
        extra_kwargs = {'slug': {'required': True}}


class TitleSerializer(serializers.ModelSerializer):
    """TitleSerializer method."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    rating = serializers.IntegerField(read_only=True)
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        """Meta class."""

        fields = '__all__'
        model = Title

    def to_representation(self, instance):
        """To_representation func."""
        response = super().to_representation(instance)
        response['genre'] = GenreSerializer(instance.genre, many=True).data
        response['category'] = CategoriesSerializer(instance.category).data
        return response


class TitleDefault:
    """TitleDefault method."""

    requires_context = True

    def __call__(self, data):
        """Call func."""
        return get_object_or_404(
            Title,
            id=data.context['view'].kwargs.get('title_id')
        )


class ReviewSerializer(serializers.ModelSerializer):
    """ReviewSerializer method."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=TitleDefault())
    score = serializers.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        """Meta class."""

        fields = '__all__'
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title']
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """CommentSerializer method."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        """Meta class."""

        model = Comment
        fields = '__all__'
        read_only_fields = ('review', )


class ValidateUsernameMixin:
    """ValidateUsernameMixin method."""

    def validate_username(self, value):
        """validate_username func."""
        return validate_username(value)


class AuthSerializer(serializers.Serializer, ValidateUsernameMixin):
    """AuthSerializer method."""

    username = serializers.CharField(
        max_length=AUTH_USERNAME_MAXLENGTH,
        required=True
    )


class RegisterSerializer(AuthSerializer):
    """RegisterSerializer method."""

    email = serializers.EmailField(
        max_length=AUTH_EMAIL_MAXLENGTH,
        required=True
    )

    class Meta:
        """Meta class."""

        model = User
        fields = ('username', 'email')


class GetTokenSerializer(AuthSerializer):
    """GetTokenSerializer method."""

    confirmation_code = serializers.CharField(
        max_length=AUTH_CONF_CODE_MAXLENGTH,
        required=True
    )

    def validate(self, data):
        """Validate func."""
        try:
            username = data.get('username')
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            raise NotFound(
                detail=f'Пользователя с именем {username} не существует.'
            )
        if user.confirmation_code != data.get('confirmation_code'):
            raise serializers.ValidationError(
                'Некорректный код подтверждения.')
        return data


class UserSerializer(serializers.ModelSerializer):
    """UserSerializer method."""

    class Meta:
        """Meta class."""

        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
