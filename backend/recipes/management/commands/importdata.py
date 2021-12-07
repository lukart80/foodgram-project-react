from django.core.management.base import BaseCommand
import json
from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('../data/ingredients.json', encoding='utf-8') as json_file:
            data = json.load(json_file)
        for ingredient in data:
            Ingredient.objects.create(
                name=ingredient['name'],
                measure_units=ingredient['measurement_unit']
                )
            print('saved!')
