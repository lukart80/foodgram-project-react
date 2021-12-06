from django.urls import path, include
from djoser.views import TokenCreateView, TokenDestroyView


urlpatterns = [
    path('api/', include('djoser.urls')),
    path('api/auth/login/', TokenCreateView.as_view(), name='login'),
    path('api/auth/logout/', TokenDestroyView.as_view(), name='logout'),

]
