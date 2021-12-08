from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import Ingredient, Tag, Recipe
from .serializers import IngredientSerializer, TagSerializer, RecipeSerializer
from .filters import IngredientFilter
from .pagination import RecipePagination


class IngredientViewSet(ReadOnlyModelViewSet):
    """View-set для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    """View-set для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = RecipePagination
