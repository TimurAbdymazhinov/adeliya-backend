from rest_framework import serializers

from drf_yasg.utils import swagger_serializer_method

from .models import (
    Banner, ProgramCondition, Contact,
    PromotionAndNews, PromotionAndNewsImage, ContactIcon,
)
from apps.notifications.models import Notification


class PromotionAndNewsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = PromotionAndNews
        fields = (
            'id',
            'created_at',
            'information_type',
            'title',
            'description',
            'is_active',
            'image',
        )

    @swagger_serializer_method(serializer_or_field=serializers.ImageField)
    def get_image(self, obj) -> str:
        image_obj = obj.images.all()
        request = self.context['request']
        image_url = request.build_absolute_uri(
            image_obj[0].image.url) if image_obj else None
        return image_url


class PromotionAndNewsImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = PromotionAndNewsImage
        fields = ('id', 'image', 'is_main',)


class PromotionAndNewsDetailSerializer(serializers.ModelSerializer):
    images = PromotionAndNewsImageSerializers(many=True)
    badge_count = serializers.SerializerMethodField()

    class Meta:
        model = PromotionAndNews
        fields = (
            'id',
            'created_at',
            'information_type',
            'title',
            'description',
            'is_active',
            'images',
            'badge_count',
        )

    @swagger_serializer_method(serializer_or_field=serializers.IntegerField)
    def get_badge_count(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            count = 0
            return count
        else:
            count = Notification.objects.filter(user=user, is_viewed=False).count()
            return count


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'title', 'description', 'image',)


class BannerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id', 'title', 'image', 'description',)


class ProgramConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramCondition
        fields = ('id', 'title', 'description',)


class ContactIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactIcon
        fields = ('id', 'title', 'image')


class ContactListSerializer(serializers.ModelSerializer):
    icon_image = ContactIconSerializer()

    class Meta:
        model = Contact
        fields = ('id', 'icon_image', 'title', 'link',)


class BannerAndPromotionSerializer(serializers.Serializer):
    banner = BannerSerializer()
    promotion = PromotionAndNewsSerializer(many=True)

    class Meta:
        field = ('banner', 'promotion',)
