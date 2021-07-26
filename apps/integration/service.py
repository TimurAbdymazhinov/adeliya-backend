import datetime
import json
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import Timeout

from django.conf import settings
from django.utils import timezone

from rest_framework import status, serializers, exceptions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from apps.account.models import User
from apps.brand.models import Filial
from apps.integration.serializers import Sync1cUserSerializer
from apps.setting.models import Setting


class User1cAuthService:
    @classmethod
    def get_response(cls, serializer) -> Response:
        """Method для login пользователя 1С"""
        user = serializer.user

        token = cls.create_or_refresh_user_token(user)
        from apps.integration.serializers import (
            Login1cAPIViewResponseSerializer
        )
        response = Login1cAPIViewResponseSerializer({
            'token': token.key,
        }).data
        return Response(
            response,
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def create_or_refresh_user_token(user: User) -> Token:
        token, created = Token.objects.get_or_create(user=user)

        return token


class CreateCheckService:
    @classmethod
    def response_user_1c_code(cls, serializer, user):
        if cls.check_qr_code_expiration_date(user):
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'message': 'Устарел QR код пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def get_user_by_qr_code(qr_code):
        user = None
        if qr_code:
            try:
                user = User.objects.get(qr_code=qr_code)
            except User.DoesNotExist:
                pass

        return user

    @staticmethod
    def check_qr_code_expiration_date(user):
        setting = Setting.objects.first()
        exp_date_limit = (
            setting.qr_code_expiration_date
            if setting else datetime.timedelta(minutes=3)
        )

        return timezone.now() - user.qr_code_updated_at <= exp_date_limit

    @staticmethod
    def get_user_and_filial_from_serializer(validated_data):
        try:
            user = User.objects.get(
                user_1C_code=validated_data['user_1c_code']
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'user_1c_code': 'Пользователь не найден'}
            )
        try:
            filial = Filial.objects.get(
                filial_1c_code=validated_data['filial_1c_code']
            )
        except Filial.DoesNotExist:
            raise serializers.ValidationError(
                {'filial_1c_code': 'Филиал не найден'}
            )

        return user, filial


REQUEST_PARAMS = {
    "auth": HTTPBasicAuth(settings.USER_1C['username'], settings.USER_1C['password']),
    "headers": {'Content-Type': 'application/json'},
    "timeout": 3
}


class User1cUpdateService:
    @classmethod
    def update_1c_user_id(cls, user):
        serialized_user = Sync1cUserSerializer(user).data
        response = cls.send_user_to_1c(serialized_user)
        response_data = cls.check_response(response, user)

        user.user_1C_code = response_data['unique_1c_user_code']
        user.save(update_fields=['user_1C_code'])

    @classmethod
    def check_response(cls, response, user):
        if response.status_code not in (200, 201):
            cls.clean_user_sign_up_data(user)
            raise exceptions.NotAcceptable(
                '1С сервер временно недоступен'
            )
        response_data = json.loads(response.text)
        if not response_data.get('unique_1c_user_code'):
            cls.clean_user_sign_up_data(user)
            raise exceptions.ValidationError(
                'Не верный формат данных из 1С сервера'
            )

        return response_data

    @staticmethod
    def send_user_to_1c(data):
        try:
            response = requests.post(
                settings.LINKS_1C['SYNC_USER_URL'],
                data=json.dumps(data),
                **REQUEST_PARAMS
            )
        except Timeout:
            raise exceptions.NotAcceptable(
                '1С сервер не отвечает'
            )

        return response

    @staticmethod
    def clean_user_sign_up_data(user):
        user.first_name = ''
        user.last_name = ''
        user.birth_date = None
        user.city = None
        user.save(update_fields=[
            'first_name', 'last_name', 'birth_date', 'city'
        ])


class UserGetWalletDataService:
    @classmethod
    def update_user_wallet_data(cls, user):
        response_data = cls.get_user_wallet_data(user)
        return response_data

    @staticmethod
    def get_user_wallet_data(user):
        response_error_data = {
            "active_point": '-',
            "inactive_point": '-',
            "discount": '-'
        }

        try:
            response = requests.get(
                settings.LINKS_1C['GET_USER_WALLET_DATA_URL'],
                params={'unique_1c_user_code': user.user_1C_code},
                **REQUEST_PARAMS
            )
        except Timeout:
            return response_error_data

        if response.status_code not in (200, 201):
            return response_error_data

        response_data = json.loads(response.text)
        if hasattr(response_data, 'err_text'):
            return response_error_data

        return response_data


class User1CNumberChangeService:
    @classmethod
    def sync_user_phone(cls, user):
        response = cls.send_user_phone(user)
        return cls.check_response(response)

    @staticmethod
    def send_user_phone(user):
        data = {
            'new_phone': user.tmp_phone,
            'unique_1c_user_code': user.user_1C_code,
        }

        try:
            response = requests.post(
                settings.LINKS_1C['CHANGE_USER_NUMBER'],
                data=json.dumps(data),
                **REQUEST_PARAMS
            )
        except Timeout:
            raise exceptions.NotAcceptable(
                '1С сервер не отвечает'
            )

        return response

    @classmethod
    def check_response(cls, response):
        if response.status_code != status.HTTP_200_OK:
            return False, 'Номер не изменен. 1C сервер не доступен'

        response_data = json.loads(response.text)
        response_is_not_success = (
                hasattr(response_data, 'err_text') or
                not response_data.get('is_changed')
        )
        if response_is_not_success:
            return False, 'Номер не изменен. Ошибка при синхронизации с 1C'

        return True, response_data
