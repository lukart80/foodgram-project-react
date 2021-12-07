from django.db import models


class Ingredient(models.Model):
    """Модель для ингредиента."""

    name = models.CharField(max_length=100, verbose_name='Название ингредиента')
    measurement_unit = models.CharField(max_length=100, verbose_name='Единицы измерения')

    class Meta:
        ordering = ('name',)
