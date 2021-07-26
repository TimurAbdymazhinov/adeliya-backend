from django.urls import path

from apps.check.views import (
    QRCodeAPIView, CheckListAPIView, CheckRetrieveAPIView
)


urlpatterns = [
    path('', CheckListAPIView.as_view(), name='check_list'),
    path('<int:pk>/', CheckRetrieveAPIView.as_view(), name='check_detail'),
    path('qr/', QRCodeAPIView.as_view(), name='qr_code'),
]
