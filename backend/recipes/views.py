from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

import weasyprint

from .filters import IngredientFilter, RecipeFilter
from .models import Cart, Favorite, Ingredient, Recipe, Tag
from .pagination import CustomPagination
from .permissions import IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
from .serializers import (CartSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeReadSerializer,
                          RecipeWithoutIngredientsSerializer,
                          RecipeWriteSerializer, TagSerializer)


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
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'create':
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]

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

            return queryset.filter(pk__in=favorite_recipes_ids)

        if self.request.GET.get('is_in_shopping_cart'):
            cart_recipes_ids = Cart.objects.filter(author=author).values('recipe_id')
            return queryset.filter(pk__in=cart_recipes_ids)
        return queryset

    @action(detail=True, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):

        author = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        payload = {
            'author': author.id,
            'recipe': recipe.id
        }
        serializer = FavoriteSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(RecipeWithoutIngredientsSerializer(
            recipe, context=self.get_serializer_context()).data,
                        status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        author = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite = get_object_or_404(Favorite, author=author, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk):

        author = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        payload = {
            'author': author.id,
            'recipe': recipe.id
        }
        serializer = CartSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(RecipeWithoutIngredientsSerializer(
            recipe, context=self.get_serializer_context()
        ).data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_item_from_shopping_cart(self, request, pk):
        author = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        cart = get_object_or_404(Cart, author=author, recipe=recipe)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        author = self.request.user
        cart_recipes = author.cart.all()

        shopping_list_dict = dict()
        for recipe in cart_recipes:
            ingredients_amount = recipe.recipe.recipe_amount.all()
            for ingredient in ingredients_amount:
                ingredient_data = shopping_list_dict.setdefault(
                    ingredient.ingredient.name, {'amount': 0,
                                                 'measurement_unit': ingredient.ingredient.measurement_unit})
                ingredient_data['amount'] += ingredient.amount

        html = render_to_string('shopping-list.html', {'shopping_list_dict': shopping_list_dict})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=shopping-list.pdf'
        weasyprint.HTML(string=html).write_pdf(response)
        return response
