from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, TagViewSet, RecipeViewSet, SubscriptionsListView

router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/subscriptions/', SubscriptionsListView.as_view(), name='subscriptions')
]
