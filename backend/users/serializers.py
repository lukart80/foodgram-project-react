from rest_framework import serializers
from .models import User, Follower


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
