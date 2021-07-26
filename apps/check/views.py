from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.account.custom_openapi import AuthRetrieveAPIView, auth_param
from apps.account.serializers import AuthErrorSerializer
from apps.brand.pagination import LargeListPagination
from apps.check.models import Check
from apps.check.serializers import (
    QRCodeSerializer, CheckListSerializer, CheckDetailSerializer
)
from apps.check.service import QRCodeService
from apps.check.filters import CheckFilter
from apps.notifications.service import SendPushNotification


class QRCodeAPIView(AuthRetrieveAPIView):
    """
        Api view for get QR code
    """
    serializer_class = QRCodeSerializer

    def get_object(self):
        return QRCodeService.update_user_data(self.request.user)


class CheckListAPIView(generics.ListAPIView):
    """
        API View for get check list
    """
    permission_classes = (IsAuthenticated,)
    pagination_class = LargeListPagination
    serializer_class = CheckListSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = CheckFilter

    def get_queryset(self):
        queryset = (
            Check.objects.filter(user=self.request.user)
        ).order_by('-accrued_point_date')

        return queryset

    @swagger_auto_schema(
        manual_parameters=[auth_param],
        responses={
            401: AuthErrorSerializer(),
        }
    )
    def get(self, request, *args, **kwargs):
        return super(CheckListAPIView, self).get(request, *args, **kwargs)


class CheckRetrieveAPIView(AuthRetrieveAPIView):
    """
        API View for get check detail
    """
    serializer_class = CheckDetailSerializer

    def get_queryset(self):
        return Check.objects.filter(user=self.request.user)

    @swagger_auto_schema(
        manual_parameters=[auth_param],
        responses={
            401: AuthErrorSerializer(),
        }
    )
    def get(self, request, *args, **kwargs):
        SendPushNotification.set_notification_viewed_for_check(
            request, self.get_object()
        )
        return super(CheckRetrieveAPIView, self).get(request, *args, **kwargs)
