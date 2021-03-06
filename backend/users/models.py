from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, username, password, first_name, last_name, is_superuser=False, is_staff=False):
        if not email:
            raise ValueError('Введите адрес электронной почты')
        if not password:
            raise ValueError('Введите пароль')
        if not username:
            raise ValueError('Введите username')
        if not first_name:
            raise ValueError('Введите имя')
        if not last_name:
            raise ValueError('Введите фамилию')

        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_superuser=is_superuser,
            is_staff=is_staff,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, first_name, last_name):
        if not email:
            raise ValueError('Введите адрес электронной почты')
        if not password:
            raise ValueError('Введите пароль')
        if not username:
            raise ValueError('Введите username')
        if not first_name:
            raise ValueError('Введите имя')
        if not last_name:
            raise ValueError('Введите фамилию')

        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_superuser=True,
            is_staff=True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """Кастомная модель пользователя."""
    email = models.EmailField(
        unique=True,
        max_length=254,
        blank=False,
        verbose_name='email'
    )

    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=150,
        blank=False,
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=False,
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']
    objects = UserManager()

    def __str__(self):
        return self.username


class Follower(models.Model):
    """Модель для подписок."""
    follower = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        blank=False,
        null=False,
    )
    following = models.ForeignKey(
        User,
        related_name='following',
        verbose_name='Подписан',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
