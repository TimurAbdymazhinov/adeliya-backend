import datetime

from rest_framework import serializers

from drf_yasg.utils import swagger_serializer_method

from apps.account.models import User
from apps.brand.models import Filial
from apps.brand.serializers import FilialImageSerializer
from apps.check.models import Check
from apps.setting.models import Setting
from apps.notifications.models import Notification


class QRCodeSerializer(serializers.ModelSerializer):
    """
        Сериализатор для QR code
        Если не найден объект Setting или не указано exp date -
        по умолчанию 3 мин
    """
    expiration_date = serializers.SerializerMethodField()

    def get_expiration_date(self, obj):
        setting = Setting.objects.first()
        if setting and setting.qr_code_expiration_date:
            return setting.qr_code_expiration_date

        return datetime.timedelta(minutes=3)

    class Meta:
        model = User
        fields = ('qr_code', 'expiration_date')
        extra_kwargs = {
            'qr_code': {'required': True},
            'expiration_date': {'required': True},
        }


class FilialListCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = ('id', 'title', 'address')


class FilialDetailCheckSerializer(serializers.ModelSerializer):
    images = FilialImageSerializer(many=True, required=False)

    class Meta:
        model = Filial
        fields = ('id', 'title', 'address', 'images')


class CheckListSerializer(serializers.ModelSerializer):
    filial = FilialListCheckSerializer()

    class Meta:
        model = Check
        fields = (
            'id', 'filial', 'accrued_point', 'accrued_point_date',
            'withdrawn_point', 'withdrawn_point_date', 'status'
        )


class CheckDetailSerializer(serializers.ModelSerializer):
    filial = FilialDetailCheckSerializer()
    badge_count = serializers.SerializerMethodField()

    class Meta:
        model = Check
        fields = (
            'id', 'filial', 'money_paid', 'bonus_paid', 'total_paid',
            'accrued_point', 'accrued_point_date', 'withdrawn_point',
            'withdrawn_point_date', 'is_active', 'status',
            'is_on_credit', 'balance_owed', 'due_date', 'badge_count',
        )

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_badge_count(self, obj):
        user = self.context['request'].user
        count = Notification.objects.filter(user=user, is_viewed=False).count()
        return count
