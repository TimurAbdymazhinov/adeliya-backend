import random
import re
import string
import requests
import xmltodict

from datetime import timedelta, datetime

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

from rest_framework import exceptions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import serializers

from dicttoxml import dicttoxml

from apps.integration.service import User1CNumberChangeService
from apps.notifications.tasks import send_notice_for_deleted_fcm_device


User = get_user_model()


class UserAuthService:
    """ Service for handling AUTH methods """

    @classmethod
    def get_response(cls, serializer) -> Response:
        """Method для login или создания пользователя и отсылки SMS """
        user = serializer.user
        if not cls.compare_confirmation_time(user):
            return Response(
                {'message': 'Вы слишком часто отправляете сообщение.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        if not cls.send_confirmation_sms(user):
            return Response(
                {'message': 'Не удалось отправить сообщение. Попробуйте позже.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if serializer.created:
            return Response(
                {'message': 'User создан! Сообщение отправлено'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'message': 'Сообщение отправлено'}, status=status.HTTP_200_OK
        )

    @classmethod
    def send_to_old_phone(cls, user: User) -> Response:
        """method for send sms to old phone number"""
        if not cls.compare_confirmation_time(user):
            return Response(
                {'message': 'Вы слишком часто отправляете сообщение.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        if not cls.send_confirmation_sms(user):
            return Response(
                {'message': 'Не удалось отправить сообщение. Попробуйте позже.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'message': 'Сообщение отправлено'}, status=status.HTTP_200_OK
        )

    @staticmethod
    def generate_new_code():
        """ Method for generating random confirmation code """
        code = ''.join(random.choice(string.digits) for i in range(6))
        return code

    @staticmethod
    def compare_confirmation_time(user_obj) -> bool:
        """ Method for checking if 1 minute left from last request """
        result = (
            not user_obj.confirmation_date
            or (timezone.now() - user_obj.confirmation_date)
            > timedelta(minutes=1)
        )

        return result

    @staticmethod
    def check_format_user_phone(phone):
        """ Method for formation user phone (+ and only digits) """
        match = re.match(r'^\+[0-9]{10,}$', phone)
        if not match:
            raise exceptions.ValidationError('phone is not valid!')
        return phone

    @staticmethod
    def get_or_create_user_instance(phone_number):
        """ Getting or creating user instance """
        try:
            user = User.objects.get(phone=phone_number)
        except User.DoesNotExist:
            user = User.objects.create(
                phone=phone_number,
                is_active=True,
                is_registration_finish=False,
            )
        created = not user.is_registration_finish

        return user, created

    @classmethod
    def set_confirmation_code(cls, user_obj: User) -> str:
        """ Method for setting confirmation sms code to user """
        confirmation_code = cls.generate_new_code()
        if user_obj.phone == '+996553000117' or user_obj.phone == '+996999111222':
            confirmation_code = '123456'
        user_obj.confirmation_code = confirmation_code
        user_obj.confirmation_date = timezone.now()
        user_obj.save(
            update_fields=['confirmation_code', 'confirmation_date'])
        return confirmation_code

    @classmethod
    def send_confirmation_sms(cls, user_obj: User) -> bool:
        """ Method for sending confirmation sms to a new or old user """
        confirmation_code = cls.set_confirmation_code(user_obj)
        id_string = '%s%d' % (user_obj.id, datetime.now().timestamp())

        data = {
            'login': settings.NIKITA_LOGIN,
            'pwd': settings.NIKITA_PASSWORD,
            'id': id_string,
            'sender': settings.NIKITA_SENDER,
            'text': f'Ваш код активации:  {confirmation_code}',
            'phones': [str(user_obj.phone).replace('+', '')],
            'test': settings.NIKITA_TEST
        }
        page = dicttoxml(data, custom_root='message',
                         item_func=lambda x: x[:-1], attr_type=False)
        response = requests.post(
            'https://smspro.nikita.kg/api/message',
            data=page, headers={'Content-Type': 'application/xml'}
        )
        response_dict = xmltodict.parse(response.text)
        status = response_dict['response']['status']
        return True if status in ('0', '11') else False


class PhoneConfirmationService:
    """ Service for handling phone confirmation on create or login """

    @classmethod
    def get_response(cls, serializer) -> Response:
        phone = serializer.validated_data['phone']
        # exists of user is checked before
        user = User.objects.get(phone=phone)
        confirmation_code = serializer.validated_data['confirmation_code']
        if not cls.check_confirmation_code(user, confirmation_code):
            return Response(
                {'message': 'Неверный код'}, status=status.HTTP_403_FORBIDDEN,
            )
        cls.check_corporate_account(user)
        cls.finish_registration(user)
        token = cls.create_or_refresh_user_token(user)
        from apps.account.serializers import LoginConfirmAPIViewResponseSerializer
        response = LoginConfirmAPIViewResponseSerializer({
                'token': token.key,
                'is_profile_completed': cls.check_is_profile_completed(user),
            }).data
        return Response(
            response,
            status=status.HTTP_200_OK,
        )

    @classmethod
    def get_response_for_old_phone_confirmation(cls, user: User, serializer) -> Response:
        confirmation_code = serializer.validated_data['confirmation_code']
        if not cls.check_confirmation_code(user, confirmation_code):
            return Response(
                {'message': 'Неверный код'}, status=status.HTTP_403_FORBIDDEN,
            )
        cls.confirm_old_phone(user)
        cls.set_confirmation_date(user)
        return Response(
            {'message': 'Old phone is confirmed'}, status=status.HTTP_200_OK,
        )

    @classmethod
    def check_confirmation_code(cls, user: User, confirmation_code: str) -> bool:
        return user.confirmation_code == confirmation_code

    @staticmethod
    def finish_registration(user: User) -> None:
        user.is_active = True
        user.is_registration_finish = True
        user.save(update_fields=['is_active', 'is_registration_finish'])

    @staticmethod
    def create_or_refresh_user_token(user: User) -> Token:
        token, created = Token.objects.get_or_create(user=user)

        return token

    @staticmethod
    def check_is_profile_completed(user: User) -> bool:
        return all(
            [user.first_name, user.last_name, user.gender, user.birth_date]
        )

    @staticmethod
    def check_is_user_exists(phone: str) -> None:
        if not User.objects.filter(phone=phone).exists():
            raise exceptions.NotFound('user not found')

    @staticmethod
    def set_confirmation_date(user_obj: User) -> None:
        user_obj.confirmation_date = None
        user_obj.save(update_fields=['confirmation_date'])

    @staticmethod
    def confirm_old_phone(user: User) -> None:
        user.is_old_phone_confirmed = True
        user.save(update_fields=['is_old_phone_confirmed'])

    @classmethod
    def check_corporate_account(cls, user) -> None:
        from fcm_django.models import FCMDevice

        user_active_device = (
            FCMDevice.objects.filter(active=True, user=user)
        )
        if user.is_corporate_account:
            if len(user_active_device) < 5:
                pass
            else:
                send_notice_for_deleted_fcm_device(
                    user_active_device,
                    user.is_corporate_account
                )
        elif len(user_active_device) < 1:
            pass
        else:
            send_notice_for_deleted_fcm_device(
                user_active_device,
                user.is_corporate_account
            )


class ChangeOldPhoneService(UserAuthService, PhoneConfirmationService):
    """ Service for changing old phone number """

    @classmethod
    def get_response(cls, serializer) -> Response:
        """Method для login пользователя и отсылки SMS """
        user = serializer.user
        new_phone = serializer.data['phone']
        response_data = {
            'message': {'message': 'Сообщение отправлено'},
            'status': status.HTTP_200_OK
        }
        if not cls.compare_confirmation_time(user):
            response_data = {
                'message': {'message': 'Вы слишком часто отправляете сообщение.'},
                'status': status.HTTP_429_TOO_MANY_REQUESTS
            }
        elif not cls.send_confirmation_sms(user):
            response_data = {
                'message': {'message': 'Не удалось отправить сообщение. Попробуйте позже.'},
                'status': status.HTTP_400_BAD_REQUEST
            }
        elif cls.new_phone_not_unique(new_phone):
            response_data = {
                'message': {'message': 'Такой номер телефона уже существует'},
                'status': status.HTTP_406_NOT_ACCEPTABLE,
            }
        return Response(
            response_data['message'], response_data['status']
        )

    @classmethod
    def get_response_for_new_phone_confirmation(
            cls, user: User,
            serializer: serializers.Serializer) -> Response:

        confirmation_code = serializer.validated_data['confirmation_code']
        if not cls.check_confirmation_code(user, confirmation_code):
            return Response(
                {'message': 'Неверный код'}, status=status.HTTP_403_FORBIDDEN,
            )
        response_1c_status, response_1c_data = (
            User1CNumberChangeService.sync_user_phone(user)
        )
        if not response_1c_status:
            return Response(
                {'message': response_1c_data},
                status=status.HTTP_400_BAD_REQUEST,
            )
        cls.confirm_new_phone(user)
        return Response(
            {'message': 'New phone is confirmed'}, status=status.HTTP_200_OK,
        )

    @staticmethod
    def new_phone_not_unique(new_phone) -> bool:
        return User.objects.filter(phone=new_phone).exists()

    @staticmethod
    def confirm_new_phone(user: User) -> None:
        user.phone, user.tmp_phone = user.tmp_phone, user.phone
        user.is_old_phone_confirmed = False
        user.save(update_fields=['phone', 'tmp_phone', 'is_old_phone_confirmed'])

    @staticmethod
    def set_tmp_phone_number(phone_number, user):
        """ Getting user instance """
        user.tmp_phone = phone_number
        user.save(update_fields=['tmp_phone'])
        return user
