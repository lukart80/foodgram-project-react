from django.contrib import admin

from .models import Favorite, Ingredient, IngredientAmount, Recipe, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка для ингредиентов."""
    list_display = ('name', 'measurement_unit')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка для тегов."""
    list_display = ('name', 'color')


class IngredientAmountInline(admin.StackedInline):
    model = IngredientAmount


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка для рецептов."""
    list_display = ('name', 'text')
    inlines = [IngredientAmountInline]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Админка для избранного."""
    list_display = ('recipe', 'author')