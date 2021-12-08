from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Ingredient, Tag
from .serializers import IngredientSerializer, TagSerializer
from .filters import IngredientFilter


class IngredientViewSet(ReadOnlyModelViewSet):
    """View-set для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    """View-set для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
