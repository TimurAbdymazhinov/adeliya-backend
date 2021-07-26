from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.check.models import Check
from apps.integration.serializers import (
    Auth1cSerializer, Get1cUserSerializer, CheckSerializer,
    Login1cAPIViewResponseSerializer, UpdateCheckSerializer,
)
from apps.integration.service import User1cAuthService, CreateCheckService
from apps.check.service import CheckNotificationService


class Auth1cAPIView(generics.GenericAPIView):
    """ Эндпоинт для login 1C пользователя """
    serializer_class = Auth1cSerializer

    @swagger_auto_schema(
        responses={
            200: Login1cAPIViewResponseSerializer(),
            400: "It will return error type",
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return User1cAuthService.get_response(serializer)


class GetUserAPIView(generics.GenericAPIView):
    """ Эндпоинт для получения unique_1C_ID пользователя по QR коду """
    serializer_class = Get1cUserSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            400: "Устарел QR код пользователя",
            404: "Пользователь не найден",
        }
    )
    def get(self, request, *args, **kwargs):
        user = CreateCheckService.get_user_by_qr_code(kwargs.get('qr_code'))
        if not user:
            return Response(
                {'message': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

        return CreateCheckService.response_user_1c_code(
            self.serializer_class(user), user
        )


class CreateCheckAPIView(generics.CreateAPIView):
    """ Эндпоинт для создание чека """
    serializer_class = CheckSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            200: CheckSerializer(),
            400: 'Ошибка при валидации',
        }
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user, filial = CreateCheckService.get_user_and_filial_from_serializer(
            serializer.validated_data
        )

        serializer.validated_data['user'] = user
        serializer.validated_data['filial'] = filial

        check = serializer.save()
        CheckNotificationService.send_notification(check, user)


class UpdateCheckAPIView(generics.UpdateAPIView):
    """ Эндпоинт для обновления чека """
    http_method_names = ('patch',)
    serializer_class = UpdateCheckSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Check.objects.all()
    lookup_field = 'unique_1c_check_code'

    @swagger_auto_schema(
        responses={
            200: UpdateCheckSerializer(),
            404: '"detail": "Страница не найдена."',
        }
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
