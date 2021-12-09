from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Ingredient, Tag, Recipe, IngredientAmount
from users.serializers import UserSerializer


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


class IngredientAmountSerializer(ModelSerializer):
    """Сериализатор промежуточной модели IngredientQuantity."""
    id = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    measurement_unit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'amount', 'measurement_unit')
        model = IngredientAmount

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class RecipeReadSerializer(ModelSerializer):
    """Сериализотор для получения рецептов."""
    image = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    author = UserSerializer()

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'name', 'image', 'text', 'id', 'ingredients', 'cooking_time',)
        read_only_fields = ['tags', 'author', 'name', 'image', 'text', 'id', 'ingredients', 'cooking_time']

    def get_image(self, obj):
        return obj.image.url

    def get_ingredients(self, obj):
        return IngredientAmountSerializer(obj.recipe_amount.all(), many=True).data
