from rest_framework import serializers
from rest_framework.serializers import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import validate_username

FORBIDDEN_NAME = 'me'
FORBIDDEN_NAME_MSG = 'Имя пользователя "me" не разрешено.'
USER_EXISTS_MSG = 'Пользователь с таким username уже зарегистрирован'
EMAIL_EXISTS_MSG = 'Указанная почта уже зарегестрирована другим пользователем'


class RegisterDataSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username],
    )
    email = serializers.EmailField(
        max_length=254,
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate_username(self, name):
        if name == FORBIDDEN_NAME:
            raise serializers.ValidationError(FORBIDDEN_NAME)
        return name

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if (
                User.objects.filter(username=username).exists()
                and User.objects.get(username=username).email != email
        ):
            raise serializers.ValidationError(USER_EXISTS_MSG)
        if (
                User.objects.filter(email=email).exists()
                and User.objects.get(email=email).username != username
        ):
            raise serializers.ValidationError(EMAIL_EXISTS_MSG)
        return data

    def create(self, validated_data):
        user, created = User.objects.get_or_create(**validated_data)
        return user


class UserRecieveTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=50)

    class Meta:
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, data):
        if data.get('username') == FORBIDDEN_NAME:
            raise serializers.ValidationError({'username': FORBIDDEN_NAME_MSG})
        return data


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
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
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
