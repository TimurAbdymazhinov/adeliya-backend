from django.urls import path
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from apps.account.views import (
    AuthAPIView, LoginConfirmAPIView, CityListAPIView,
    UserUpdateAPIView, UserAvatarRetrieveUpdateAPIView,
    SendSmsToOldPhoneAPIView, OldPhoneConfirmAPIView,
    ChangeOldPhoneAPIView, NewPhoneConfirmAPIView, UserRetrieveAPIView
)

urlpatterns = [
    path('auth/', AuthAPIView.as_view(), name='auth'),
    path('login-confirm/', LoginConfirmAPIView.as_view(), name='login-confirm'),
    path('send-sms-to-old-phone/', SendSmsToOldPhoneAPIView.as_view(), name='send_sms_to_old_phone'),
    path('old-phone-confirm/', OldPhoneConfirmAPIView.as_view(), name='old_phone_confirm'),

    path('change-old-phone/', ChangeOldPhoneAPIView.as_view(), name='change_old_phone'),
    path('new-phone-confirm/', NewPhoneConfirmAPIView.as_view(), name='new_phone_confirm'),

    path('cities/', CityListAPIView.as_view(), name='cities'),
    path('', UserUpdateAPIView.as_view(), name='update'),
    path('data/', UserRetrieveAPIView.as_view(), name='retrieve'),
    path('avatar/', UserAvatarRetrieveUpdateAPIView.as_view(), name='avatar'),

    path(
        'device/', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}),
        name='create_fcm_device',
    ),
    path(
        'device/<str:registration_id>/',
        FCMDeviceAuthorizedViewSet.as_view({'delete': 'destroy',
                                            'put': 'update'}),
        name='delete_fcm_device',
    ),
]
