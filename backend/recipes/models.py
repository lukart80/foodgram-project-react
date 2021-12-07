from django.db import models


# Create your models here.

class Ingredient(models.Model):
    """Модель для ингредиента."""

    name = models.CharField(max_length=100, verbose_name='Название ингредиента')
    measure_units = models.CharField(max_length=100, verbose_name='Единицы измерения')

    class Meta:
        ordering = ('name',)
