from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Recipe

from .models import Follower, User


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
        data = {
            'email': instance.email,
            'id': instance.id,
            'username': instance.username,
            'first_name': instance.first_name,
            'last_name': instance.last_name
        }
        return data


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
                fields=('follower', 'following'),
                message='Подписка уже существует'
            )
        ]

    def validate_follower(self, value):
        if self.context.get('request').user.pk == value:
            raise ValidationError('Подписка на самого себя!')
        return value


class ResetPasswordSerializer(serializers.Serializer):
    """Сериализатор для изменения пароля."""
    new_password = serializers.CharField(required=True, read_only=True)
    current_password = serializers.CharField(required=True, read_only=True)

    def validate_current_password(self, value):
        user = self.context.get('request').user
        if user.check_password(value):
            return value
        raise ValidationError('Неверный пароль пользователя!')

