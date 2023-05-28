from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from rest_framework import serializers

from api.mixins import Base64ImageField
from api.utils import check_anonymous_return_bool
from recipes.models import (Cart, Favorite, IngredientInRecipe, Ingredients,
                            Recipes, Tags)


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


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов"""

    class Meta:
        model = Tags
        fields = '__all__'


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов"""

    class Meta:
        model = Ingredients
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор связанной модели ингредиентов и рецептов"""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipesSerializer(serializers.ModelSerializer):
    """Сериализатор Recipes для создания, обновления и удаления рецептов"""

    tags = TagsSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source='ingredientinrecipe_set',
        many=True,
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    name = serializers.CharField(
        required=True, max_length=settings.RECIPE_NAME
    )
    image = Base64ImageField(
        max_length=None,
        required=True,
        allow_null=False,
        allow_empty_file=False
    )
    text = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(
        required=True,
    )

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def validate(self, data):
        """Валидируем ингредиенты и теги"""
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                {'ingredients': 'Нужен хотя бы один ингредиент для рецепта'}
            )
        ingredients_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(
                Ingredients, id=ingredient_item['id']
            )
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    {'ingredients': 'Ингредиенты не должны повторяться'}
                )
            ingredients_list.append(ingredient)
        tags = self.initial_data.get('tags')
        if not tags:
            raise serializers.ValidationError(
                {'tags': 'Нужен хотя бы один тэг для рецепта'}
            )
        tags_list = []
        for tag_item in tags:
            tag = get_object_or_404(Tags, id=tag_item)
            if tag in tags_list:
                raise serializers.ValidationError(
                    {'tags': 'Теги в рецепте не должны повторяться'}
                )
            tags_list.append(tag)

        data['author'] = self.context.get('request').user
        data['ingredients'] = ingredients
        data['tags'] = tags
        return data

    def create_ingredients(self, ingredients, recipe):
        """Создание связки ингредиентов для рецепта"""
        for ingredient_item in ingredients:
            IngredientInRecipe.objects.bulk_create(
                [IngredientInRecipe(
                    ingredient_id=ingredient_item['id'],
                    recipe=recipe,
                    amount=ingredient_item['amount']
                )]
            )

    @transaction.atomic
    def create(self, validated_data):
        """Создаем рецепт"""
        image = validated_data.pop('image')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipes.objects.create(image=image, **validated_data)
        recipe.tags.clear()
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        recipe.save()
        return recipe

    @transaction.atomic
    def update(self, recipe, validated_data):
        """Обновляем рецепт"""
        recipe.ingredients.clear()
        self.create_ingredients(validated_data.pop('ingredients'), recipe)
        tags = validated_data.pop('tags')
        recipe.tags.clear()
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)

    def delete(self, recipe):
        """Удаляем рецепт"""
        recipe.delete()

    def get_is_favorited(self, obj):
        """Получаем статус добавления рецепта в избанное"""
        if check_anonymous_return_bool(
            self.context.get('request'),
            obj,
            Favorite
        ):
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        """Получаем статус списка покупок"""
        if check_anonymous_return_bool(
            self.context.get('request'),
            obj,
            Cart
        ):
            return True
        return False
