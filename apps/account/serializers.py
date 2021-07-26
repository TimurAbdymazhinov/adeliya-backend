from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from apps.account.models import User, City
from apps.account.service import (
    UserAuthService, PhoneConfirmationService, ChangeOldPhoneService,
)
from apps.integration.service import UserGetWalletDataService
from apps.notifications.models import Notification
from apps.setting.models import HelpPage
from apps.setting.serializers import HelpPageSerializer


class PhoneAuthSerializer(serializers.Serializer):
    """Сериалайзер для валидации и создания пользователя """
    phone = serializers.CharField(required=True)

    def validate(self, data):
        self.user, self.created = (
            UserAuthService.get_or_create_user_instance(phone_number=data.get('phone'))
        )
        if not self.created:
            self.confirm_login_allowed(self.user)
        return data

    def validate_phone(self, value):
        UserAuthService.check_format_user_phone(value)
        return value

    @staticmethod
    def confirm_login_allowed(user):
        if not user.is_active:
            raise serializers.ValidationError({'phone': 'Этот номер не активен.'})


class ConfirmationCodeSerializer(serializers.Serializer):
    """Serializer for phone code confirmation"""
    confirmation_code = serializers.CharField(max_length=6, required=True)


class LoginConfirmationCodeSerializer(PhoneAuthSerializer, ConfirmationCodeSerializer):
    """ Сериалайзер для login код подтверждения """

    def validate(self, data):
        PhoneConfirmationService.check_is_user_exists(data.get('phone'))
        self.confirm_login_allowed(data.get('phone'))
        return data

    def validate_phone(self, value):
        super(LoginConfirmationCodeSerializer, self).validate_phone(value)
        PhoneConfirmationService.check_is_user_exists(value)
        return value

    @staticmethod
    def confirm_login_allowed(phone: str) -> None:
        if not User.objects.filter(phone=phone, is_active=True).exists():
            raise serializers.ValidationError({'phone': 'Этот номер не активен.'})


class ChageOldPhoneSerializer(PhoneAuthSerializer):
    """ Сериалайзер для login код подтверждения """

    def validate(self, data):
        request = self.context['request']
        self.user = (
            ChangeOldPhoneService.set_tmp_phone_number(
                phone_number=data.get('phone'),
                user=request.user,
            )
        )
        return data

    def validate_phone(self, value):
        return ChangeOldPhoneService.check_format_user_phone(value)


class LoginConfirmAPIViewResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    is_profile_completed = serializers.BooleanField()


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'title']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'birth_date', 'city']
        extra_kwargs = {
            field: {'required': True} for field in fields
        }


class UserAvatarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar']
        extra_kwargs = {'avatar': {'required': True}}


class AuthErrorSerializer(serializers.Serializer):
    """ Error response on status.HTTP_401_UNAUTHORIZED """
    detail = serializers.CharField(help_text='This is error text')


class UserGetWalletSerializer(serializers.Serializer):
    """ Serializer for user wallet data """
    discount = serializers.CharField(required=True)
    active_point = serializers.CharField(required=True)
    inactive_point = serializers.CharField(required=True)


class UserRetrieveSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    has_notification = serializers.SerializerMethodField()
    wallet = serializers.SerializerMethodField()
    help_page = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'first_name', 'phone', 'avatar', 'last_name', 'gender',
            'birth_date', 'city', 'has_notification', 'wallet', 'help_page',
        ]

    @swagger_serializer_method(serializer_or_field=UserGetWalletSerializer)
    def get_wallet(self, obj):
        user_wallet_data = UserGetWalletDataService.update_user_wallet_data(obj)
        serializer = UserGetWalletSerializer(data=user_wallet_data)
        serializer.is_valid(raise_exception=True)

        return serializer.data

    @swagger_serializer_method(serializer_or_field=HelpPageSerializer)
    def get_help_page(self, obj):
        help_page_obj = HelpPage.objects.first()
        serializer = HelpPageSerializer(help_page_obj)
        return serializer.data

    def get_city(self, obj):
        return obj.city.title if obj.city else None

    def get_has_notification(self, obj):
        return Notification.objects.filter(user=obj, is_viewed=False).exists()
