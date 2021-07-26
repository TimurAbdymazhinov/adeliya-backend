from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.account.models import User
from apps.brand.models import Filial
from apps.check.models import Check


class Auth1cSerializer(serializers.ModelSerializer):
    """Сериалайзер для валидации пользователя 1c"""

    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')
        if phone and password:
            user = authenticate(request=self.context.get('request'),
                                phone=phone, password=password)
            if not user:
                raise serializers.ValidationError(
                    {'Сообщение': 'Некорректные данные'})
        else:
            raise serializers.ValidationError(
                {'Сообщение': 'Неверный формат данных'})

        self.user = user

        return data

    class Meta:
        model = User
        fields = ('phone', 'password')


class Login1cAPIViewResponseSerializer(serializers.Serializer):
    """
        Сериалайзер для токена пользователя 1c
    """
    token = serializers.CharField()


class Get1cUserSerializer(serializers.ModelSerializer):
    """
        Сериализатор 1С данных пользователя
    """

    class Meta:
        model = User
        fields = ('user_1C_code', 'phone')
        extra_kwargs = {
            'user_1C_code': {'required': True},
            'phone': {'required': True}
        }


class CheckSerializer(serializers.ModelSerializer):
    """Сериалайзер для чека"""
    user_1c_code = serializers.CharField(required=True)
    filial_1c_code = serializers.CharField(required=True)

    class Meta:
        model = Check
        fields = (
            'unique_1c_check_code', 'money_paid', 'bonus_paid', 'total_paid',
            'accrued_point', 'accrued_point_date', 'withdrawn_point',
            'withdrawn_point_date', 'is_active', 'user_1c_code',
            'filial_1c_code', 'status', 'is_on_credit', 'balance_owed',
            'due_date',
        )


class UpdateCheckSerializer(serializers.ModelSerializer):
    """Сериалайзер обновления для чека"""

    class Meta:
        model = Check
        fields = (
            'money_paid', 'bonus_paid', 'total_paid',
            'accrued_point', 'accrued_point_date',
            'withdrawn_point', 'withdrawn_point_date',
            'is_active',  'status', 'is_on_credit', 'balance_owed','due_date',
        )


class Sync1cUserSerializer(serializers.ModelSerializer):
    """
        Сериализатор для синхронизации 1С данных пользователя
    """

    class Meta:
        model = User
        fields = (
            'phone', 'first_name', 'last_name', 'gender',
            'birth_date'
        )
