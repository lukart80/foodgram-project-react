from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from .models import User, Follower
from .serializers import UserSerializer, FollowingReadSerializer, UserCreateSerializer, FollowingCreateSerializer
from recipes.pagination import CustomPagination


class UserViewSet(ModelViewSet):
    """View-set для работы с пользователями."""
    queryset = User.objects.all()

    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return UserSerializer
        if self.action == 'create':
            return UserCreateSerializer

    @action(methods=['GET'], detail=False)
    def me(self, request):
        return Response(UserSerializer(request.user, context=self.get_serializer_context()).data)

    @action(methods=['GET'], detail=True)
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


class SubscriptionsListView(ListAPIView):
    """View-класс для просмотра подписчиков."""
    serializer_class = FollowingReadSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        user_following_ids = user.follower.all().values('following')
        return User.objects.filter(pk__in=user_following_ids)

