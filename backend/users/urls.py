from django.urls import path, include
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, SubscriptionsListView

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('api/users/subscriptions/', SubscriptionsListView.as_view(), name='subscriptions'),
    path('api/', include(router.urls)),
    path('api/auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('api/auth/token/logout/', TokenDestroyView.as_view(), name='logout'),


]
