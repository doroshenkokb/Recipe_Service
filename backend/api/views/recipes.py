from django.db.models import Count, Sum
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import IngredientsFilter, RecipesFilterSet
from api.mixins import FavoriteCart
from api.permissions import IsAdminAuthorOrReadOnly
from api.serializers.recipes import (IngredientsSerializer, RecipesSerializer,
                                     ShortSerializer, TagsSerializer)
from api.utils import download_pdf
from recipes.models import (Cart, Favorite, IngredientInRecipe, Ingredients,
                            Recipes, Tags)


class IngredientsViewSet(ReadOnlyModelViewSet):
    """Вьюсет для модели Ingredients"""

    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()
    permission_classes = (AllowAny,)
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

    def get_queryset(self):
        """Получаем queryset рецептов с аннотацией recipes_count"""
        return self.annotate_recipes_count(super().get_queryset())

    def annotate_recipes_count(self, queryset):
        """Аннотируем queryset рецептов с количеством рецептов автора"""
        return queryset.annotate(recipes_count=Count('author__recipe_author'))

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
