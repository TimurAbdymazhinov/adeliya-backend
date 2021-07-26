from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.notifications.service import NotificationResponseService


class LargeListNotificationPagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        reformat_data = NotificationResponseService.reformat(data)
        return Response({
            'count': self.page.paginator.count,
            'next': self.page.next_page_number() if self.page.has_next() else None,
            'previous': self.page.previous_page_number() if self.page.has_previous() else None,
            'results': reformat_data,
        })
