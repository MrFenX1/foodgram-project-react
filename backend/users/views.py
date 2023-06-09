from rest_framework import status, views, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from users.serializers import (GetTokenSerializer,
                               UserSerializer,
                               ChangePasswordSerializer,
                               SubscriptionSerializer)
from users.models import CustomUser, Subscribe


class UserViewsSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """Эндпоинт ./users/"""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


    @action(methods=['GET'],
            detail=False,
            url_path='me')
    def me(self, request):
        """Метод получения данных о себе
        Эндпоинт ./users/me/"""

        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)

            return Response(serializer.data)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['POST'],
            detail=False,
            url_path='set_password')
    def set_password(self, request):
        """Метод изменения пароля пользхователя
        Эндпоинт ./users/set_password/"""

        serializer = ChangePasswordSerializer(request.user,
                                              data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST','DELETE'],
            permission_classes=[IsAuthenticated],
            url_path=r'(?P<id>[\d]+)/subscribe',
            url_name='subscribe',
            detail=False)
    def subscribe(self, request, **kwargs):
        """Метод подписки и отписки от пользователя
        Эндпоинт ./users/<id>/subscribe/"""
        user = request.user
        author_id = kwargs.get('id')
        author = get_object_or_404(CustomUser, id=author_id)
        subscription = Subscribe.objects.filter(
            user=user.id,
            user_author=author_id
        )

        if self.request.method == 'POST' and not subscription.exists():
            serializer = SubscriptionSerializer(
                author,
                data=request.data,
                context={'request': self.request}
            )
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(user=user,
                                     user_author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if self.request.method == 'DELETE' and subscription.exists():
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Ошибка'},
            status=status.HTTP_400_BAD_REQUEST
        )


    # def subscribe(self, request, **kwargs):
    #     if request.method == 'POST':
    #         author = get_object_or_404(CustomUser, id=id)
    #         serializer = SubscriptionSerializer(author, data=request.data, context={'request': request})
    #         if serializer.is_valid():
    #             serializer.save(user=request.user)
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         author = get_object_or_404(CustomUser, id=id)
    #         subscription = Subscribe.objects.filter(user=request.user.id, user_author=id)
    #         if subscription.exists():
    #             subscription.delete()
    #             return Response(status=status.HTTP_204_NO_CONTENT)
    #         return Response({'error': 'Ошибка'}, status=status.HTTP_400_BAD_REQUEST)

    @action(permission_classes=[IsAuthenticated],
            serializer_class=SubscriptionSerializer,
            methods=['GET'],
            detail=False)
    def subscriptions(self, request):
        """Метод просмотра подписчиков
        Эндпоинт ./users/subscriptions/"""
        queryset = CustomUser.objects.filter(
            author__user=request.user
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)


class GetTokenView(ObtainAuthToken):
    """
    Обработка только POST запроса для получения токена по email и паролю.
    """
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        """
        Метод создания токена.
        """
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            CustomUser, email=serializer.validated_data['email']
        )
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'auth_token': token.key
            },
            status=status.HTTP_201_CREATED
        )


class DeleteTokenViews(views.APIView):
    """ Обработка  POST запроса и удаления токена"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Метод удаления Токена"""
        token = request.auth
        token.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
