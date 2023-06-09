from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from api.utils import check_anonymous_return_bool
from recipes.models import Recipes
from users.models import Follow, User


class UsersCreateSerializer(UserCreateSerializer):
    """Сериализатор для обработки запросов на создание пользователя.
    Валидирует создание пользователя с юзернеймом 'me'."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def validate_username(self, value):
        if value == "me":
            raise ValidationError(
                'Невозможно создать пользователя с таким именем!'
            )
        return value


class UsersSerializer(UserSerializer):
    """Сериализатор для отображения информации о пользователе."""

    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Получаем статус подписки на автора"""
        return check_anonymous_return_bool(self, obj, Follow)


class FollowSerializer(UsersSerializer):
    """Сериализатор для добавления/удаления подписки, просмотра подписок."""

    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        """Получаем рецепты, на которые подписаны и ограничиваем по лимитам"""
        queryset = Recipes.objects.filter(author=obj.author)
        recipes_limit = self.context.get('request').GET.get('recipes_limit')
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        return ShortSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        """Считаем рецепты автора, на которого подписан пользователь"""
        return obj.author.recipe_author.count()


class ShortSerializer(serializers.ModelSerializer):
    """Сериализатор короткого ответа рецептов для подписок и избранного"""

    class Meta:
        model = Recipes
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
