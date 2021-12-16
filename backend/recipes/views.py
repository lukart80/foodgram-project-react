from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import Ingredient, Tag, Recipe, IngredientAmount, Favorite
from .serializers import IngredientSerializer, TagSerializer, RecipeReadSerializer, RecipeWriteSerializer
from .filters import IngredientFilter, RecipeFilter
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
    filterset_class = RecipeFilter
    pagination_class = RecipePagination

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeReadSerializer
        elif self.action == 'create' or self.action == 'update':
            return RecipeWriteSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Recipe.objects.all()
        author = self.request.user
        if self.request.GET.get('is_favorited'):
            favorite_recipes_ids = Favorite.objects.filter(author=author).values('recipe_id')

            return queryset.filter(author=author, pk__in=favorite_recipes_ids)
        return queryset
