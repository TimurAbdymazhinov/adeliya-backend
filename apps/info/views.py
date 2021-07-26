from django.db.models import Prefetch

from rest_framework.response import Response
from rest_framework.viewsets import generics
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema

from apps.brand.pagination import SmallListPagination
from core.constants import PROMOTION
from .models import (
    Banner,
    ProgramCondition,
    Contact,
    PromotionAndNews, PromotionAndNewsImage,
)
from .serializers import (
    ProgramConditionSerializer,
    ContactListSerializer,
    BannerDetailSerializer,
    BannerAndPromotionSerializer,
    PromotionAndNewsSerializer,
    PromotionAndNewsDetailSerializer,
)
from apps.notifications.service import SendPushNotification


class BannerRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerDetailSerializer

    def get_object(self):
        return self.get_queryset().first()


class BannerAndPromotionAPIView(generics.RetrieveAPIView):
    """
        API view for banner and promotion
    """
    serializer_class = BannerAndPromotionSerializer

    def retrieve(self, request, *args, **kwargs):
        banner = Banner.objects.first()
        promotion = (
            PromotionAndNews.objects.filter(
                is_active=True,
                information_type=PROMOTION
            ).prefetch_related(
                Prefetch('images', PromotionAndNewsImage.objects.filter(
                    is_main=True
                ))
            )[:3]
        )
        banner_and_promotion = dict(
            banner=banner,
            promotion=promotion,
        )
        serializer = self.get_serializer(banner_and_promotion)
        return Response(serializer.data)


class ProgramConditionAPIView(generics.RetrieveAPIView):
    """
       API view for ProgramCondition
    """
    queryset = ProgramCondition.objects.all()
    serializer_class = ProgramConditionSerializer

    def get_object(self):
        return self.get_queryset().first()


class ContactListAPIView(generics.ListAPIView):
    """
        API list view for contact
    """
    queryset = Contact.objects.all()
    serializer_class = ContactListSerializer


class PromotionAndNewsListAPIView(generics.ListAPIView):
    """
        API list view for promotions and news
    """
    queryset = (
        PromotionAndNews.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                'images', PromotionAndNewsImage.objects.filter(is_main=True)
            )
        )
    )
    serializer_class = PromotionAndNewsSerializer
    pagination_class = SmallListPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['information_type']
    permission_classes = [AllowAny]


class PromotionAndNewsRetrieveAPIView(generics.RetrieveAPIView):
    """
        API detail view for promotions and news
    """
    queryset = PromotionAndNews.objects.all()
    serializer_class = PromotionAndNewsDetailSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            404: '{"detail": "Страница не найдена."}',
        }
    )
    def get(self, request, *args, **kwargs):
        SendPushNotification.set_notification_viewed_for_article(
            request, self.get_object()
        )
        return super(PromotionAndNewsRetrieveAPIView, self).get(request, *args, **kwargs)
