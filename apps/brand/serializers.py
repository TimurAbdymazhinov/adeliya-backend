from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from apps.brand.models import (
    Brand, BrandImage, FilialImage, FilialPhone, Filial
)
from apps.brand.service import FilialService, WorkDayService


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'logo')


class BrandImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandImage
        fields = ('id', 'image')


class BrandDetailSerializer(serializers.ModelSerializer):
    images = BrandImageSerializer(many=True, required=False)

    class Meta:
        model = Brand
        fields = ('title', 'description', 'address', 'link', 'images')


class FilialImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilialImage
        fields = ('id', 'image', 'is_main')


class FilialPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilialPhone
        fields = ('id', 'phone', 'is_phone', 'is_whatsapp')


class GeolocationSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    long = serializers.FloatField()


class FilialSerializer(serializers.ModelSerializer):
    images = FilialImageSerializer(many=True, required=False)
    phone_numbers = FilialPhoneSerializer(many=True, required=False)
    is_filial_open = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()
    geolocation = serializers.SerializerMethodField()
    week_days = serializers.SerializerMethodField()

    class Meta:
        model = Filial
        fields = (
            'title', 'address', 'geolocation', 'distance', 'images',
            'phone_numbers', 'is_filial_open', 'week_days',
        )

    def get_is_filial_open(self, obj) -> bool:
        return FilialService.check_filial_status(obj)

    def get_distance(self, obj) -> float:
        client_geolocation = self.context.get('client_geolocation')

        return FilialService.calculate_distance(
            filial_geolocation=obj.geolocation,
            client_geolocation=client_geolocation
        )

    @swagger_serializer_method(serializer_or_field=serializers.ListField)
    def get_week_days(self, obj):
        data = WorkDayService.get_weekday(obj)
        return data

    @swagger_serializer_method(serializer_or_field=GeolocationSerializer)
    def get_geolocation(self, obj):
        if obj.geolocation:
            lat, long = tuple(map(float, obj.geolocation.split(',')))
            data = {'lat': lat, 'long': long}
            serializer = GeolocationSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            return serializer.data

        return None


class FilialListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    is_filial_open = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Filial
        fields = (
            'position', 'id', 'title', 'address', 'distance',
            'is_filial_open', 'image'
        )

    @swagger_serializer_method(serializer_or_field=serializers.ImageField)
    def get_image(self, obj):
        image_obj = obj.images.all()
        request = self.context['request']
        image_url = request.build_absolute_uri(image_obj[0].image.url) if image_obj else None
        return image_url

    def get_is_filial_open(self, obj) -> bool:
        return FilialService.check_filial_status(obj)

    def get_distance(self, obj) -> float:
        client_geolocation = self.context.get('client_geolocation')

        return FilialService.calculate_distance(
            filial_geolocation=obj.geolocation,
            client_geolocation=client_geolocation
        )
