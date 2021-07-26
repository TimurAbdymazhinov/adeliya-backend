from django.db.models import Prefetch

from rest_framework import generics

from drf_yasg.utils import swagger_auto_schema

from apps.brand import custom_openapi
from apps.brand.models import Brand, Filial, FilialImage
from apps.brand.pagination import LargeListPagination, SmallListPagination
from apps.brand.serializers import (
    BrandListSerializer, BrandDetailSerializer, FilialListSerializer,
    FilialSerializer,
)
from apps.brand.service import FilialService


class BrandListAPIView(generics.ListAPIView):
    """
        Api view for get all brand list page by 20
    """
    serializer_class = BrandListSerializer
    queryset = Brand.objects.all()
    pagination_class = LargeListPagination


class BrandRetrieveAPIView(generics.RetrieveAPIView):
    """
        Api view for get brand by id
    """
    serializer_class = BrandDetailSerializer
    queryset = Brand.objects.all()
    lookup_field = 'id'

    @swagger_auto_schema(
        responses={
            404: '{"detail": "Страница не найдена."}',
        }
    )
    def get(self, request, *args, **kwargs):
        return super(BrandRetrieveAPIView, self).get(request, *args, **kwargs)


class FilialListAPIView(generics.ListAPIView):
    """
        Api view for get all filial list page by 10
    """
    serializer_class = FilialListSerializer
    pagination_class = SmallListPagination
    queryset = (
        Filial.objects.all()
        .prefetch_related(
            Prefetch('images', FilialImage.objects.filter(is_main=True))
        )
    )

    def get_serializer_context(self):
        context = super(FilialListAPIView, self).get_serializer_context()
        client_geolocation = FilialService.get_geolocation(self.request)
        context['client_geolocation'] = client_geolocation

        return context

    @swagger_auto_schema(
        manual_parameters=custom_openapi.filial_extra_params,
        responses={
            400: '{"geolocation": "Неправильный формат query param: lat long"}',
        }
    )
    def get(self, request, *args, **kwargs):
        return super(FilialListAPIView, self).get(request, *args, **kwargs)


class FilialRetrieveAPIView(generics.RetrieveAPIView):
    """
        Api view for get filial by id
    """
    serializer_class = FilialSerializer
    queryset = Filial.objects.all()
    lookup_field = 'id'

    def get_serializer_context(self):
        context = super(FilialRetrieveAPIView, self).get_serializer_context()
        client_geolocation = FilialService.get_geolocation(self.request)
        context['client_geolocation'] = client_geolocation

        return context

    @swagger_auto_schema(
        manual_parameters=custom_openapi.filial_extra_params,
        responses={
            400: '{"geolocation": "Неправильный формат query param: lat long"}',
            404: '{"detail": "Страница не найдена."}',
        }
    )
    def get(self, request, *args, **kwargs):
        return super(FilialRetrieveAPIView, self).get(request, *args, **kwargs)
