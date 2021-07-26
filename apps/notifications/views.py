from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.notifications.models import Notification
from apps.notifications.pagination import LargeListNotificationPagination
from apps.notifications.serializers import NotificationSerializer


class NotificationAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = LargeListNotificationPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = (
            Notification.objects.filter(is_active=True, user=self.request.user)
        )

        return queryset
