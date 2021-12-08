from django.db import models


class Ingredient(models.Model):
    """Модель для ингредиента."""

    name = models.CharField(max_length=100, verbose_name='Название ингредиента', blank=False, null=False)
    measurement_unit = models.CharField(max_length=100, verbose_name='Единицы измерения', blank=False, null=False)

    class Meta:
        ordering = ('name',)


class Tag(models.Model):
    """Модель для тегов."""

    name = models.CharField(max_length=200, verbose_name='Название', blank=False, null=False)
    color = models.CharField(max_length=7, verbose_name='Код цвета')
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ('name',)