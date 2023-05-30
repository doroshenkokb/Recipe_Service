from colorfield.fields import ColorField
from django.conf import settings
from django.db import models

from users.models import User


class Ingredients(models.Model):
    """Модель ингредиентов"""

    name = models.CharField(
        'Название',
        max_length=settings.INGREDIENTS,
        db_index=True
    )
    measurement_unit = models.CharField(
        'Ед. измерения',
        max_length=settings.INGREDIENTS
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'ингредиенты'
        verbose_name_plural = 'ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return self.name


class Tags(models.Model):
    """Модель тэгов"""

    name = models.CharField(
        'Название тега',
        max_length=settings.TAG_SLUG_NAME,
        unique=True
    )
    color = ColorField(
        'Цвет',
        format='hex',
        max_length=settings.TAG_COLOR,
        unique=True
    )
    slug = models.SlugField(
        'Ссылка',
        max_length=settings.TAG_SLUG_NAME,
        unique=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'тэг'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Recipes(models.Model):
    """Модель рецептов"""

    name = models.CharField(
        'Название рецепта',
        max_length=settings.RECIPE_NAME
    )
    text = models.TextField('Описание')
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/%Y/%m/%d/'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
    )
    tags = models.ManyToManyField(Tags, verbose_name='теги')
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe_author',
        verbose_name='Автор'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """Модель ингредиентов в рецепте"""

    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique ingredient in recipe'
            )
        ]

    def __str__(self):
        return f'{self.ingredient}'


class Favorite(models.Model):
    """Модель избранного"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='favorite_unique'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'Пользователь:{self.user.username}, рецепт: {self.recipe.name}'


class Cart(models.Model):
    """Модель списка покупок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='cart_unique'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return f'{self.recipe} в списке покупок у {self.user}'
