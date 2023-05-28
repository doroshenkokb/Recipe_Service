from django_filters import rest_framework as filters
from django_filters.rest_framework import FilterSet
from rest_framework.filters import SearchFilter

from recipes.models import Recipes
from users.models import User


class IngredientsFilter(SearchFilter):
    """Полнотекстовый поиск по ингредиентам"""

    def get_search_fields(self, view, request):
        if request.query_params.get('name'):
            return ['name']
        return super().get_search_fields(view, request)

    search_param = 'name'


class RecipesFilterSet(FilterSet):
    """Фильтр рецептов по тегам, авторам, избранному, подпискам"""

    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited',
        field_name='favorite__user'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_shopping_cart',
        field_name='cart__user'
    )

    def filter_is_favorited(self, queryset, name, value):
        """Фильтрация по избранному"""
        if value:
            return queryset.filter(**{name: self.request.user})
        return queryset

    def filter_shopping_cart(self, queryset, name, value):
        """Фильтрация по списку покупок"""
        if value:
            return queryset.filter(**{name: self.request.user})
        return queryset

    class Meta:
        model = Recipes
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart'
        )
