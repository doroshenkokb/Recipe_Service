from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

# from api.mixins import SubscriptionListView
from api.permissions import IsAdminAuthorOrReadOnly
from api.serializers.users import FollowSerializer, UsersSerializer
from users.models import Follow, User


class UsersViewSet(UserViewSet):
    """Вьюсет для работы с пользователями и подписками.
    Обработка запросов на создание/получение пользователей и
    создание/получение/удаления подписок."""

    queryset = User.objects.all() 
    serializer_class = UsersSerializer 
    permission_classes = (IsAuthenticatedOrReadOnly,) 
 
    def get_permissions(self): 
        if self.action == 'me': 
            self.permission_classes = (IsAuthenticated,) 
        return super().get_permissions() 


    @action(
        methods=['post', 'delete'],
        detail=True, permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        """Функция подписки и отписки."""
        user = request.user
        author = get_object_or_404(User, pk=id)
        obj = Follow.objects.filter(user=user, author=author)
        if request.method == 'POST':
            if user == author:
                return Response({'errors': 'На себя подписаться нельзя'},
                                status=status.HTTP_400_BAD_REQUEST
                                )
            if obj.exists():
                return Response(
                    {'errors': f'Вы уже подписаны на {author.username}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FollowSerializer(
                Follow.objects.create(user=user, author=author),
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if user == author:
            return Response(
                {'errors': 'Вы не можете отписаться от самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': f'Вы уже отписались от {author.username}'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        # return SubscriptionListView.as_view()(request)
        serializer = FollowSerializer(
            self.paginate_queryset(
                Follow.objects.filter(user=request.user)
            ), many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
