from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from .models import User, Follower
from recipes.models import Recipe


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False

        return Follower.objects.filter(follower=user, following=obj).exists()


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя."""
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def to_representation(self, instance):
        return UserSerializer(instance, context=self.context).data


class RecipeWithoutIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецепта без ингредиентов."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowingReadSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода авторов, на которых подписан пользователь."""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'recipes', 'is_subscribed', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Follower.objects.filter(follower=self.context['request'].user, following=obj).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        if request.GET.get('recipes_limit'):
            recipes = recipes[:int(request.GET.get('recipes_limit'))]
        serializer = RecipeWithoutIngredientsSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()


class FollowingCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания подписки."""

    class Meta:
        model = Follower
        fields = ('follower', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follower.objects.all(),
                fields=('follower', 'following')
            )
        ]

    def validate_follower(self, value):
        if self.context.get('request').user.pk == value:
            raise ValidationError('Подписка на самого себя!')
        return value


