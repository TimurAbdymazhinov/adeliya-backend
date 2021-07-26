from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.account.custom_openapi import (
    AuthRetrieveAPIView, AuthUpdateAPIView, auth_param,
)
from apps.account.models import City
from apps.account.serializers import (
    PhoneAuthSerializer, LoginConfirmationCodeSerializer, CitySerializer,
    UserUpdateSerializer, LoginConfirmAPIViewResponseSerializer,
    UserAvatarUpdateSerializer, AuthErrorSerializer, ConfirmationCodeSerializer,
    ChageOldPhoneSerializer, UserRetrieveSerializer,
)
from apps.account.service import (
    UserAuthService, PhoneConfirmationService, ChangeOldPhoneService
)
from apps.integration.service import User1cUpdateService


class AuthAPIView(generics.GenericAPIView):
    """ Эндпоинт для login или создания пользователя и отсылки SMS """
    serializer_class = PhoneAuthSerializer

    @swagger_auto_schema(
        responses={
            200: '{"message": "Сообщение отправлено"}',
            201: '{"message": "User создан! Сообщение отправлено"}',
            400: "It will return error type",
            429: '{"message": "Вы слишком часто отправляете сообщение."}',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return UserAuthService.get_response(serializer)


class LoginConfirmAPIView(generics.GenericAPIView):
    """ Endpoint для подтверждения номера и авторизации пользователя """
    serializer_class = LoginConfirmationCodeSerializer

    @swagger_auto_schema(
        responses={
            200: LoginConfirmAPIViewResponseSerializer(),
            400: 'It will return error type',
            403: '{"message": "Неверный код"}',
            404: '{"detail": "user not found"}',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return PhoneConfirmationService.get_response(serializer)


class SendSmsToOldPhoneAPIView(generics.GenericAPIView):
    """ Endpoint for send sms to old phone number """
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        manual_parameters=[auth_param],
        responses={
            200: '{"message": "Сообщение отправлено"}',
            400: "It will return error type",
            401: AuthErrorSerializer(),
            429: '{"message": "Вы слишком часто отправляете сообщение."}',
        }
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        return UserAuthService.send_to_old_phone(user)


class OldPhoneConfirmAPIView(generics.GenericAPIView):
    """ Endpoint для подтверждения old phone number """
    permission_classes = (IsAuthenticated,)
    serializer_class = ConfirmationCodeSerializer

    @swagger_auto_schema(
        manual_parameters=[auth_param],
        responses={
            200: '{"message": "Old phone is confirmed"}',
            400: 'It will return error type',
            401: AuthErrorSerializer(),
            403: '{"message": "Неверный код"}',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        return PhoneConfirmationService.get_response_for_old_phone_confirmation(user, serializer)


class ChangeOldPhoneAPIView(generics.GenericAPIView):
    """ Endpoint для смены old phone number """
    permission_classes = (IsAuthenticated,)
    serializer_class = ChageOldPhoneSerializer

    @swagger_auto_schema(
        responses={
            200: '{"message": "Сообщение отправлено"}',
            400: "It will return error type",
            406: "{'message': 'Такой номер телефона уже существует'}",
            429: '{"message": "Вы слишком часто отправляете сообщение."}',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        return ChangeOldPhoneService.get_response(serializer)


class NewPhoneConfirmAPIView(generics.GenericAPIView):
    """ Endpoint для подтверждения new phone number """
    permission_classes = (IsAuthenticated,)
    serializer_class = ConfirmationCodeSerializer

    @swagger_auto_schema(
        manual_parameters=[auth_param],
        responses={
            200: '{"message": "New phone is confirmed"}',
            400: 'It will return error type',
            401: AuthErrorSerializer(),
            403: '{"message": "Неверный код"}',
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        return ChangeOldPhoneService.get_response_for_new_phone_confirmation(user, serializer)


class CityListAPIView(generics.ListAPIView):
    """Endpoint for get city list"""
    queryset = City.objects.all()
    serializer_class = CitySerializer


class UserUpdateAPIView(AuthUpdateAPIView):
    """Endpoint for update user"""
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save()
        User1cUpdateService.update_1c_user_id(user)


class UserRetrieveAPIView(AuthRetrieveAPIView):
    """Endpoint for update user"""
    serializer_class = UserRetrieveSerializer

    def get_object(self):
        return self.request.user


class UserAvatarRetrieveUpdateAPIView(AuthRetrieveAPIView, AuthUpdateAPIView,
                                      generics.DestroyAPIView):
    """Endpoint for update user image"""
    serializer_class = UserAvatarUpdateSerializer

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.avatar = None
        instance.save(update_fields=['avatar'])
        return Response(status=status.HTTP_204_NO_CONTENT)
