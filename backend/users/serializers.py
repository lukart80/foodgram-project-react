from djoser.serializers import UserCreateSerializer
from .models import User

class CustomUserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer):
        fields = ('email', 'username', 'password', 'first_name', 'last_name')
        model = User
