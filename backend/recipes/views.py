from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import Ingredient, Tag, Recipe, IngredientAmount
from .serializers import IngredientSerializer, TagSerializer, RecipeReadSerializer, RecipeWriteSerializer
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

    pagination_class = RecipePagination

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeReadSerializer
        elif self.action == 'create':
            return RecipeWriteSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)
