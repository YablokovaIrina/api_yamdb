from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import SlugRelatedField

from api_yamdb.settings import (
    EMAIL_LENGHT,
    MAX_LENGHT,
    MAX_LENGHT_CODE
)
from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import validate_username


class RegisterDataSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGHT,
        validators=[validate_username],
    )
    email = serializers.EmailField(
        max_length=EMAIL_LENGHT,
    )


class UserRecieveTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGHT,
        validators=[validate_username],
    )
    confirmation_code = serializers.CharField(max_length=MAX_LENGHT_CODE)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        return validate_username(value)


class CommentSerializer(serializers.ModelSerializer):

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data
        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs.get('title_id')
        )
        author = self.context['request'].user

        if Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError('Вы уже оставили отзыв')
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id', )
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id', )
        model = Genre
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(required=False)

    class Meta:
        fields = '__all__'
        model = Title
        read_only_fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',)


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
