from django.urls import path

from apps.notifications.views import NotificationAPIView


urlpatterns = [
    path('', NotificationAPIView.as_view(), name='notification_list'),
]
