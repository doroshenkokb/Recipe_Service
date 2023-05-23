from django.contrib import admin

from recipes.models import Cart, Favorite, Ingredients, Recipes, Tags


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('id', 'name', 'color', 'slug')
    list_filter = ('name', 'color')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('id', 'name')
    list_filter = ('measurement_unit',)


class IngredientInRecipeInline(admin.TabularInline):
    model = Recipes.ingredients.through
    min_num = 1
    autocomplete_fields = ('ingredient',)
    fields = (
        'id', 'ingredient', 'amount', 'get_measurement_unit'
    )
    readonly_fields = ('get_measurement_unit',)

    @admin.display(description='Ед. измерения')
    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'author', 'get_ingredients', 'get_favorites_count',
        'get_shopping_cart_count'
    )
    search_fields = ('id', 'name', 'tags', 'ingredients')
    list_filter = ('name', 'tags', 'author')
    autocomplete_fields = ('author', 'tags')
    inlines = [IngredientInRecipeInline]

    @admin.display(description='Ингредиенты')
    def get_ingredients(self, obj):
        return list(Recipes.objects.filter(id=obj.id).values_list(
            'ingredients__name', flat=True).order_by('-ingredients__name'))

    @admin.display(description='Добавили в избранное')
    def get_favorites_count(self, obj):
        return obj.favorite.count()

    @admin.display(description='Добавили в список покупок')
    def get_shopping_cart_count(self, obj):
        return obj.cart.count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('recipe',)
    autocomplete_fields = ('user', 'recipe')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('recipe',)
    autocomplete_fields = ('user', 'recipe')
