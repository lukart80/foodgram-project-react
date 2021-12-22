from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recipes.pagination import CustomPagination

from .models import Follower, User
from .serializers import (FollowingCreateSerializer, FollowingReadSerializer,
                          UserCreateSerializer, UserSerializer, ResetPasswordSerializer)


class UserViewSet(ModelViewSet):
    """View-set для работы с пользователями."""
    queryset = User.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return UserSerializer
        if self.action == 'create':
            return UserCreateSerializer

    @action(methods=['GET'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        return Response(UserSerializer(request.user, context=self.get_serializer_context()).data)

    @action(methods=['GET'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, pk):
        follower = request.user
        following = get_object_or_404(User, pk=pk)
        payload = {
            'follower': follower.pk,
            'following': following.pk
        }
        serializer = FollowingCreateSerializer(data=payload, context=self.get_serializer_context())

        if serializer.is_valid():
            serializer.save()
            return Response(FollowingReadSerializer(following, context=self.get_serializer_context()).data)
        return Response(serializer.errors)

    @subscribe.mapping.delete
    def unfollow(self, request, pk):
        follower = request.user
        following = get_object_or_404(User, pk=pk)
        Follower.objects.get(following=following, follower=follower).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def set_password(self, request):
        user = request.user
        serializer = ResetPasswordSerializer(data=request.data, context=self.get_serializer_context())
        if serializer.is_valid():
            user.set_password(request.data['new_password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionsListView(ListAPIView):
    """View-класс для просмотра подписчиков."""
    serializer_class = FollowingReadSerializer
    pagination_class = CustomPagination
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        user_following_ids = user.follower.all().values('following')
        return User.objects.filter(pk__in=user_following_ids)
