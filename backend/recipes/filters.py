import django_filters

from users.models import User

from .models import Ingredient, Recipe


class IngredientFilter(django_filters.FilterSet):
    """Фильтр для ингредиентов."""
    name = django_filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    """Фильтр для рецпетов."""
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = django_filters.ModelChoiceFilter(
        queryset=User.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

