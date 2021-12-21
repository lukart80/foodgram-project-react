import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Команда для наполнения базы данных ингредиентами из файла. Ввести 'pyhon manage.py importdata'."""
    def handle(self, *args, **options):
        with open('data/ingredients.json', encoding='utf-8') as json_file:
            data = json.load(json_file)
        for ingredient in data:
            Ingredient.objects.create(
                name=ingredient['name'],
                measurement_unit=ingredient['measurement_unit']
                )

