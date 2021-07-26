from django.urls import path, include

from apps.integration.views import (
    Auth1cAPIView, GetUserAPIView, CreateCheckAPIView, UpdateCheckAPIView
)

urlpatterns = [
    path('user/', include([
        path('login/', Auth1cAPIView.as_view(), name='login-1c'),
        path(
            '<str:qr_code>/', GetUserAPIView.as_view(),
            name='get_user_by_qr_code'
        ),
    ])),
    path('check/', include([
        path('', CreateCheckAPIView.as_view(), name='create_check'),
        path(
            '<str:unique_1c_check_code>/', UpdateCheckAPIView.as_view(),
            name='update_check_view'
        ),
    ])),
]
