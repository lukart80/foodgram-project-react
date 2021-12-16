from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from users.models import User
from .models import Ingredient, Tag, Recipe, Favorite, Cart
from .serializers import IngredientSerializer, TagSerializer, RecipeReadSerializer, RecipeWriteSerializer, \
    FavoriteSerializer, CartSerializer, FollowingReadSerializer
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

        if self.request.GET.get('is_in_shopping_cart'):
            cart_recipes_ids = Cart.objects.filter(author=author).values('recipe_id')
            return queryset.filter(author=author, pk__in=cart_recipes_ids)
        return queryset

    @action(detail=True, methods=['GET'])
    def favorite(self, request, pk):

        author = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        payload = {
            'author': author.id,
            'recipe': recipe.id
        }
        serializer = FavoriteSerializer(data=payload)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        author = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite = get_object_or_404(Favorite, author=author, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['GET'])
    def shopping_cart(self, request, pk):

        author = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        payload = {
            'author': author.id,
            'recipe': recipe.id
        }
        serializer = CartSerializer(data=payload)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_item_from_shopping_cart(self, request, pk):
        author = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        cart = get_object_or_404(Cart, author=author, recipe=recipe)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsListView(ListAPIView):
    serializer_class = FollowingReadSerializer
    pagination_class = RecipePagination

    def get_queryset(self):
        user = self.request.user
        user_following_ids = user.follower.all().values('following')
        return User.objects.filter(pk__in=user_following_ids)
