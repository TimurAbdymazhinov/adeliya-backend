from apps.setting.service import ApplicationStatusService


class ApplicationStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return ApplicationStatusService.check_application_status(
            request, response
        )
