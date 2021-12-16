from abc import ABC

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer
from drf_extra_fields.fields import Base64ImageField
from .models import Ingredient, Tag, Recipe, IngredientAmount, Favorite
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


class IngredientAmountReadSerializer(ModelSerializer):
    """Сериализатор для чтения данных из промежуточной модели IngredientAmount."""
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
    ingredients = serializers.SerializerMethodField()
    author = UserSerializer()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'name', 'image', 'text', 'id', 'ingredients', 'cooking_time', 'is_favorited')
        read_only_fields = ['tags', 'author', 'name', 'image', 'text', 'id', 'ingredients', 'cooking_time']

    def get_image(self, obj):
        return obj.image.url

    def get_ingredients(self, obj):
        return IngredientAmountReadSerializer(obj.recipe_amount.all(), many=True).data

    def get_is_favorited(self, obj):
        author = self.context.get('request').user
        if not author.is_authenticated:
            return False
        if Favorite.objects.filter(author=author, recipe=obj):
            return True
        return False


class IngredientAmountWriteSerializer(serializers.Serializer):
    """Сериализатор для записи ингредиентов в рецепт."""
    amount = serializers.IntegerField(write_only=True)
    id = serializers.IntegerField(write_only=True)


class RecipeWriteSerializer(ModelSerializer):
    """Сериализатор для создания рецепта."""
    image = Base64ImageField(required=True)

    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientAmountWriteSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'image', 'tags', 'text', 'cooking_time', 'ingredients')

    def create(self, validated_data):
        ingredients = self.validated_data.pop('ingredients')
        tags = self.initial_data.get('tags')
        recipe = Recipe.objects.create(**validated_data)
        for tag_id in tags:
            recipe.tags.add(get_object_or_404(Tag, pk=tag_id))
        for ingredient in ingredients:
            ingredient_instance = get_object_or_404(Ingredient, pk=ingredient.get('id'))
            IngredientAmount.objects.create(
                recipe=recipe,
                ingredient=ingredient_instance,
                amount=ingredient.get('amount')
            )
        return recipe

    def update(self, instance, validated_data, partial=True):
        tags = self.initial_data.get('tags')
        ingredients = self.validated_data.get('ingredients')
        instance.tags.clear()
        for tag_id in tags:
            instance.tags.add(get_object_or_404(Tag, pk=tag_id))

        IngredientAmount.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            ingredient_instance = get_object_or_404(Ingredient, pk=ingredient.get('id'))
            IngredientAmount.objects.create(
                ingredient=ingredient_instance,
                amount=ingredient.get('amount'),
                recipe=instance
            )

        instance.name = validated_data.get('name')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.image = validated_data.get('image')
        instance.text = validated_data.get('text')
        instance.save()

        return instance
