from django.http import JsonResponse
from rest_framework import status

from apps.setting.models import Setting


class ApplicationStatusService:
    @classmethod
    def check_application_status(cls, request, response):
        app_setting = Setting.objects.first()
        is_service_off = (
            app_setting and
            not app_setting.is_service_active and
            cls.is_api_path(request)
        )
        if is_service_off:
            return JsonResponse(
                {'message': 'Сервис временно недоступен'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return response

    @staticmethod
    def is_api_path(request):
        return True if request.path.split('/')[1] == 'api' else False
