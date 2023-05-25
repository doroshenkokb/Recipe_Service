from django.db.models import Sum
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import IngredientsFilter, RecipesFilterSet
from api.permissions import IsAdminAuthorOrReadOnly
from api.utils import download_pdf
from recipes.models import (Cart, Favorite,
                            IngredientInRecipe, Ingredients,
                            Recipes, Tags)
from recipes.serializers import (IngredientsSerializer, RecipesSerializer,
                                 ShortSerializer, TagsSerializer)
from .mixins import FavoriteCart
from users.models import Follow, User
from users.serializers import FollowSerializer, UsersSerializer


class CustomUserViewSet(UserViewSet):
    """Вьюсет для модели User и Follow"""

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminAuthorOrReadOnly]
    pagination_class = PageNumberPagination

    @action(
        methods=['get'], detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        """Получить данные текущего пользователя"""
        return Response(
            UsersSerializer(
                get_object_or_404(User, id=request.user.id)
            ).data,
            status=status.HTTP_200_OK
        )

    @action(
        methods=['get'], detail=False,
        permission_classes=[IsAuthenticated],
        pagination_class=PageNumberPagination
    )
    def subscriptions(self, request):
        """Получить подписки пользователя"""
        serializer = FollowSerializer(
            self.paginate_queryset(
                Follow.objects.filter(user=request.user)
            ), many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True, permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        """Функция подписки и отписки."""
        user = request.user
        author = get_object_or_404(User, pk=id)
        obj = Follow.objects.filter(user=user, author=author)
        if request.method == 'POST':
            if user == author:
                return Response(
                    {'errors': 'На себя подписаться нельзя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if obj.exists():
                return Response(
                    {'errors': f'Вы уже подписаны на {author.username}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FollowSerializer(
                Follow.objects.create(user=user, author=author),
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if user == author:
            return Response(
                {'errors': 'Вы не можете отписаться от самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': f'Вы уже отписались от {author.username}'},
            status=status.HTTP_400_BAD_REQUEST
        )


class IngredientsViewSet(ReadOnlyModelViewSet):
    """Вьюсет для модели Ingredients"""

    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()
    permission_classes = [IsAdminAuthorOrReadOnly]
    pagination_class = None
    filter_backends = [IngredientsFilter]
    search_fields = ('^name',)


class TagsViewSet(ReadOnlyModelViewSet):
    """Вьюсет для модели Tags"""

    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    permission_classes = [IsAdminAuthorOrReadOnly]
    pagination_class = None


class RecipesViewSet(ModelViewSet, FavoriteCart):
    """Вьюсет для модели Recipes, Favorite и Cart"""

    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminAuthorOrReadOnly]
    filter_class = RecipesFilterSet
    add_serializer = ShortSerializer
    add_model = Recipes

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        """Функция добавления и удаления избранного."""
        errors = {
            'if_exists': 'Рецепт уже добавлен в избранное',
            'if_deleted': 'Вы уже удалили рецепт из избранного'
        }
        return self.favorite_and_cart(request, pk, Favorite, errors)

    @action(
        methods=['post', 'delete'],
        detail=True, permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        """Функция добавления и удаления рецептов в/из списка покупок."""
        errors = {
            'if_exists': 'Рецепт уже добавлен в список покупок',
            'if_deleted': 'Вы уже удалили рецепт из списка покупок'
        }
        return self.favorite_and_cart(request, pk, Cart, errors)

    @action(
        methods=['get'], detail=False, permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """Скачать список покупок в pdf"""
        ingredients = IngredientInRecipe.objects.filter(
            recipe__cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(Sum('amount')).order_by()
        if ingredients:
            return download_pdf(ingredients)
        return Response(
            {'errors': 'Нет рецептов в списке покупок'},
            status=status.HTTP_400_BAD_REQUEST
        )
