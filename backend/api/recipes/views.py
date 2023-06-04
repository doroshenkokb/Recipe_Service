from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import IngredientsFilter, RecipesFilterSet
from api.mixins import FavoriteCart
from api.permissions import AuthorOrReadOnly
from api.recipes.serializers import (FavoriteSerializer, IngredientsSerializer,
                                     RecipeGETSerializer, RecipeSerializer,
                                     ShoppingCartSerializer, ShortSerializer,
                                     TagsSerializer)
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
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipesViewSet(ModelViewSet, FavoriteCart):
    """Вьюсет для модели Recipes, Favorite и Cart"""

    queryset = Recipes.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, AuthorOrReadOnly
    )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilterSet
    add_serializer = ShortSerializer
    add_model = Recipes

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='favorite',
        url_name='favorite',
        permission_classes=(IsAuthenticated,)
    )
    def get_favorite(self, request, pk):
        """Позволяет текущему пользователю добавлять рецепты в избранное."""
        recipe = get_object_or_404(Recipes, pk=pk)
        if request.method == 'POST':
            serializer = FavoriteSerializer(
                data={'user': request.user.id, 'recipe': recipe.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            favorite_serializer = ShortSerializer(recipe)
            return Response(
                favorite_serializer.data, status=status.HTTP_201_CREATED
            )
        favorite_recipe = get_object_or_404(
            Favorite, user=request.user, recipe=recipe
        )
        favorite_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='shopping_cart',
        url_name='shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def get_shopping_cart(self, request, pk):
        """Позволяет текущему пользователю добавлять рецепты
        в список покупок."""
        recipe = get_object_or_404(Recipes, pk=pk)
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(
                data={'user': request.user.id, 'recipe': recipe.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            shopping_cart_serializer = ShortSerializer(recipe)
            return Response(
                shopping_cart_serializer.data, status=status.HTTP_201_CREATED
            )
        shopping_cart_recipe = get_object_or_404(
            Cart, user=request.user, recipe=recipe
        )
        shopping_cart_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Позволяет текущему пользователю загрузить список покупок."""
        shopping_cart = Cart.objects.filter(user=request.user)
        ingredients_cart = IngredientInRecipe.objects.filter(
            recipe__in=shopping_cart.values('recipe')
        )
        ingredients_cart = ingredients_cart.values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(ingredient_value=Sum('amount'))
        ingredients_cart = ingredients_cart.order_by('ingredient__name')
        ingredients_cart = ingredients_cart.values_list(
            'ingredient__name',
            'ingredient__measurement_unit',
            'ingredient_value'
        )
        return download_pdf(ingredients_cart)

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        if self.request.method == 'GET':
            return RecipeGETSerializer
        return RecipeSerializer
