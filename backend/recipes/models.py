from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import constraints

User = get_user_model()


class Ingredient(models.Model):
    """Модель для ингредиента."""

    name = models.CharField(max_length=100, verbose_name='Название ингредиента', blank=False, null=False)
    measurement_unit = models.CharField(max_length=100, verbose_name='Единицы измерения', blank=False, null=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name[:20]


class Tag(models.Model):
    """Модель для тегов."""

    name = models.CharField(max_length=200, verbose_name='Название', blank=False, null=False)
    color = models.CharField(max_length=7, verbose_name='Код цвета')
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name[:20]


class Recipe(models.Model):
    """Модель для рецептов."""

    tags = models.ManyToManyField(Tag, verbose_name='Теги', related_name='recipes')
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='recipes')
    name = models.CharField(max_length=200, verbose_name='Название', blank=False, null=False)
    image = models.ImageField(upload_to='recipes/', blank=False, null=False)
    text = models.CharField(max_length=3000, verbose_name='Описание', blank=False, null=False)
    cooking_time = models.PositiveIntegerField(verbose_name='Время пригототовления', blank=False, null=False)
    ingredients = models.ManyToManyField(Ingredient, through='IngredientAmount', related_name='recipes', )

    def __str__(self):
        return self.name[:20]


class IngredientAmount(models.Model):
    """Промежуточная модель для хранения количесва ингредиентов."""
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='рецепт',
                               blank=False, null=False,
                               related_name='recipe_amount')
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='recipe_amount'
                                   )
    amount = models.PositiveIntegerField(blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'], name='unique_ingredient_recipe')
        ]


class Favorite(models.Model):
    """Модель для избранных рецептов пользователя."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=True,
        verbose_name='Пользователь',
        related_name='favorites'
    )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               verbose_name='Рецепт',
                               related_name='favorites',
                               )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'recipe'], name='unique_favorite')
        ]


class Cart(models.Model):
    """Модель для корзины рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=True,
        verbose_name='Пользователь',
        related_name='cart'
    )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               verbose_name='Рецепт',
                               related_name='cart',
                               )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'recipe'], name='unique_cart'),
        ]