from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.account.serializers import AuthErrorSerializer

auth_param = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description='Token ...',
    type=openapi.TYPE_STRING
)


class AuthUpdateAPIView(generics.UpdateAPIView):
    """UpdateAPIView for Authenticated endpoints"""
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        manual_parameters=[auth_param],
        responses={
            401: AuthErrorSerializer(),
            400: 'It will return error type',
        }
    )
    def put(self, request, *args, **kwargs):
        return super(AuthUpdateAPIView, self).put(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[auth_param],
        responses={
            401: AuthErrorSerializer(),
            400: 'It will return error type',
        }
    )
    def patch(self, request, *args, **kwargs):
        return super(AuthUpdateAPIView, self).patch(request, *args, **kwargs)


class AuthRetrieveAPIView(generics.RetrieveAPIView):
    """RetrieveAPIView for Authenticated endpoints"""
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        manual_parameters=[auth_param],
        responses={
            401: AuthErrorSerializer(),
        }
    )
    def get(self, request, *args, **kwargs):
        return super(AuthRetrieveAPIView, self).get(request, *args, **kwargs)
