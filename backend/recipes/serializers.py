from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Ingredient, Tag, Recipe


class IngredientSerializer(ModelSerializer):
    """Сериализатор для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(ModelSerializer):
    """"Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(ModelSerializer):
    """Сериализотор для рецептов."""
    image = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'name', 'image', 'text', 'id', 'ingredients', 'cooking_time')

    def get_image(self, obj):
        return obj.image.url
